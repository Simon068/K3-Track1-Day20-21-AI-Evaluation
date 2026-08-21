"""Chấm results.jsonl bằng LLM judge -> verdicts.jsonl, rồi đối chiếu labels.csv.

Cách dùng (chạy từ root repo):
  python3 eval/judge.py                # prompt/output mặc định
  python3 eval/judge.py sc-01 sc-03    # chỉ chấm các scenario_id được chọn
  python3 eval/judge.py --prompt eval/judge_prompts/groundedness-v1.md \
      --output verdicts-groundedness-v1.jsonl --labels labels-groundedness.csv
Judge dùng prompt trong eval/judge_prompt.md (placeholder {{input}} {{answer}} {{sources}}).
Model judge mặc định khác model tutor (EVAL_JUDGE_MODEL, mặc định openai/gpt-4o-mini)
để tránh tự chấm chéo cùng một model.
"""
import argparse, csv, json, os, sys, time
from pathlib import Path

# tutor.py nằm ở tutor/ (khu vực sản phẩm) — thêm vào sys.path để import được
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tutor"))

import tutor
import tracing

# --- Tracing (tuỳ chọn): Braintrust hoặc LangSmith, log mỗi verdict thành 1 trace
_tracer = tracing.init_tracer()

JUDGE_MODEL = os.environ.get("EVAL_JUDGE_MODEL", "openai/gpt-4o-mini")
JUDGE_MAX_TOKENS = int(os.environ.get("EVAL_JUDGE_MAX_TOKENS", "2000"))
JUDGE_DELAY_S = float(os.environ.get("EVAL_JUDGE_DELAY_S", "0"))
_default_reasoning_effort = (
    "minimal" if JUDGE_MODEL.startswith("openrouter/openai/gpt-5") else None
)
JUDGE_REASONING_EFFORT = os.environ.get(
    "EVAL_JUDGE_REASONING_EFFORT", _default_reasoning_effort
)

# judge_prompt.md nằm cạnh file này trong eval/ — resolve theo __file__, không theo cwd
PROMPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "judge_prompt.md")
FATAL_PROVIDER_STATUSES = {401, 402, 403, 429}


def provider_http_status(error):
    """Lấy HTTP status từ lỗi requests mà không phụ thuộc trực tiếp vào requests."""
    return getattr(getattr(error, "response", None), "status_code", None)


def parse_judge_output(content):
    """Judge bắt buộc trả JSON; output bị cắt không phải verdict uncertain."""
    out = tutor.parse_json_content(content)
    if out.get("_parse_error"):
        raise RuntimeError("judge trả output không parse được JSON hoặc bị cắt giữa chừng")
    return out

def read_jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def read_labels(path="labels.csv"):
    """labels.csv: scenario_id,label,note — chỉ lấy dòng có label."""
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return {r["scenario_id"]: r["label"].strip().lower()
                for r in csv.DictReader(f) if r.get("label", "").strip()}

def build_judge_prompt(rec, template):
    """Nhồi input/answer/sources của 1 row vào template.
    Nếu row có slide context thì gắn vào input — judge phải chấm theo đúng
    bối cảnh học viên đang đứng ở slide nào."""
    input_text = rec.get("input", "")
    if rec.get("slide"):
        input_text = tutor.format_slide_context(rec["slide"]).strip() + "\n" + input_text
    answer = json.dumps(rec.get("output"), ensure_ascii=False, indent=2)
    sources = json.dumps(rec.get("output", {}).get("sources", []),
                         ensure_ascii=False, indent=2)
    return (template.replace("{{input}}", input_text)
                    .replace("{{answer}}", answer)
                    .replace("{{sources}}", sources))

def judge_row(rec, template, criterion="unspecified"):
    prompt = build_judge_prompt(rec, template)
    data, latency = tutor.chat([{"role": "user", "content": prompt}],
                               model=JUDGE_MODEL, max_tokens=JUDGE_MAX_TOKENS,
                               reasoning_effort=JUDGE_REASONING_EFFORT)
    choice = data["choices"][0]
    content = (choice.get("message") or {}).get("content")
    if not isinstance(content, str) or not content.strip():
        reasoning_tokens = (data.get("usage", {})
                                .get("completion_tokens_details", {})
                                .get("reasoning_tokens"))
        raise RuntimeError(
            "judge trả content rỗng "
            f"(finish_reason={choice.get('finish_reason')!r}, "
            f"reasoning_tokens={reasoning_tokens!r}, "
            f"max_tokens={JUDGE_MAX_TOKENS}). "
            "Tăng EVAL_JUDGE_MAX_TOKENS hoặc dùng model judge không tiêu tốn "
            "toàn bộ budget cho reasoning."
        )
    out = parse_judge_output(content)
    return {"scenario_id": rec["scenario_id"], "criterion": criterion,
            "verdict": out.get("verdict", "uncertain"),
            "score": out.get("score"), "rationale": out.get("rationale", ""),
            "issues": out.get("issues", []), "raw_content": content,
            "usage": data.get("usage", {}), "latency_s": round(latency, 2)}

def print_confusion(verdicts, labels):
    """Ma trận nhầm lẫn judge (hàng) vs nhãn người (cột) + tỉ lệ đồng thuận."""
    classes = ["pass", "fail", "uncertain"]
    infra_errors = [v for v in verdicts if v.get("error")]
    pairs = [(v["verdict"], labels[v["scenario_id"]])
             for v in verdicts
             if not v.get("error") and v["scenario_id"] in labels]
    if infra_errors:
        print("\nLoại %d row lỗi hạ tầng khỏi confusion matrix: %s" %
              (len(infra_errors), ", ".join(v["scenario_id"] for v in infra_errors)))
    if not pairs:
        print("\nlabels.csv chưa có nhãn nào trùng scenario_id -> chưa tính được agreement.")
        print("Mở report.html, gán nhãn rồi bấm 'Export labels.csv' để có nhãn người.")
        return
    print("\nConfusion matrix (hàng = judge, cột = nhãn người):")
    print("%10s | %s" % ("", " ".join("%9s" % c for c in classes)))
    for cj in classes:
        row = [sum(1 for v, h in pairs if v == cj and h == ch) for ch in classes]
        print("%10s | %s" % (cj, " ".join("%9d" % x for x in row)))
    agree = sum(1 for v, h in pairs if v == h)
    print("Agreement: %d/%d = %.0f%%" % (agree, len(pairs), 100.0 * agree / len(pairs)))

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Chạy một LLM judge cho đúng một tiêu chí.")
    parser.add_argument("scenario_ids", nargs="*", help="Để trống = chấm mọi row")
    parser.add_argument("--prompt", default=PROMPT_PATH, help="File prompt của tiêu chí")
    parser.add_argument("--output", default="verdicts.jsonl", help="File JSONL kết quả")
    parser.add_argument("--labels", default="labels.csv", help="Gold labels cùng tiêu chí")
    parser.add_argument("--criterion", help="Tên tiêu chí; mặc định lấy từ tên prompt")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    results = read_jsonl("results.jsonl")
    if not results:
        sys.exit("Không thấy results.jsonl — chạy python3 eval/run_eval.py trước.")
    if not tutor.get_api_key(JUDGE_MODEL):
        sys.exit("Chưa có API key cho judge model %s — xem .env.example." % JUDGE_MODEL)
    if not os.path.exists(args.prompt):
        sys.exit("Không thấy judge prompt: %s" % args.prompt)
    chosen = set(args.scenario_ids)
    rows = [r for r in results if not chosen or r["scenario_id"] in chosen]
    rows = [r for r in rows if "output" in r]  # bỏ row lỗi, không có gì để chấm
    template = open(args.prompt, encoding="utf-8").read()
    criterion = args.criterion or Path(args.prompt).stem
    print("Chấm %d row, tiêu chí %s, judge %s ..." %
          (len(rows), criterion, JUDGE_MODEL))

    verdicts = []
    for i, rec in enumerate(rows, 1):
        print("[%d/%d] %s ... " % (i, len(rows), rec["scenario_id"]), end="", flush=True)
        try:
            v = judge_row(rec, template, criterion)
            _tracer.log_run(
                name="judge-run",
                inputs={"scenario_id": rec["scenario_id"], "judge_model": JUDGE_MODEL,
                        "criterion": criterion, "prompt_file": args.prompt},
                outputs={"verdict": v["verdict"], "rationale": v.get("rationale", "")},
                metrics={**{k: x for k, x in v.get("usage", {}).items()
                            if isinstance(x, (int, float))},
                         "latency_s": v.get("latency_s", 0)},
            )
            print(v["verdict"])
        except Exception as e:
            status = provider_http_status(e)
            if status in FATAL_PROVIDER_STATUSES:
                reason = ("provider rate-limit/quota" if status == 429
                          else "provider từ chối xác thực/thanh toán")
                print("LỖI FATAL HTTP %s: %s." % (status, reason))
                if _tracer.backend:
                    _tracer.flush()
                sys.exit(
                    "Dừng run; kiểm tra API key, quota hoặc credit. "
                    "Không ghi file verdict vì đây là lỗi hạ tầng, không phải verdict uncertain."
                )
            v = {"scenario_id": rec["scenario_id"], "verdict": "uncertain",
                 "error": str(e)}
            print("LỖI: %s" % e)
        verdicts.append(v)
        if JUDGE_DELAY_S > 0 and i < len(rows):
            time.sleep(JUDGE_DELAY_S)

    with open(args.output, "w", encoding="utf-8") as f:
        for v in verdicts:
            f.write(json.dumps(v, ensure_ascii=False) + "\n")
    print("Ghi %d verdict vào %s" % (len(verdicts), args.output))
    if _tracer.backend:
        _tracer.flush()
        print("Đã log %d trace judge lên %s." % (len(verdicts), _tracer.backend))
    print_confusion(verdicts, read_labels(args.labels))

if __name__ == "__main__":
    main()
