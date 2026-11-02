"""Codex evidence amendment and independent structural audit. Standard library only.

Explicit anchors below were read against the original page text. A missing
anchor is an error; there is no fallback to an unrelated first source span.
Original Antigravity artifacts, raw answers, gold and production code stay intact.
"""
import collections
import hashlib
import json
import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
ROOT = SRC.parent
RESULTS = SRC / 'evaluation/results'
PAGES = ROOT / '02_Dữ Liệu Quy Chế/04_Dữ Liệu Đã Kiểm Chứng/QD580/QD580_PAGES.jsonl'
def jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]

pages = {r['pdf_page']: r['content'] for r in jsonl(PAGES)}
chunks = {r['chunk_id']: r for r in jsonl(SRC/'data/QD580_CHUNKS.jsonl')}
shorts = {re.search(r'_(c\d+)_', cid).group(1): c for cid,c in chunks.items()}
raw = {(r['mode'],r['case_id']):r for r in jsonl(RESULTS/'DNC_RAG_AB_DEV10_TASK05.jsonl')}
gold = {r['id']:r for r in jsonl(SRC/'evaluation/DEV_10_CAU_QD580.jsonl')}
original = jsonl(RESULTS/'EVIDENCE_DEV10_TASK05_R05.jsonl')

# Each entry is a complete point's support, potentially across pages/chunks.
# Missing retrieved gold support is recorded separately, never inserted into context.
anchors = {
 'DEV01-P1':[('c061',15,77,434)],
 'DEV01-P2':[('c062',15,436,858)],
 'DEV01-P3':[('c062',15,436,858)],
 'DEV01-P4':[('c061',15,77,434)],
 'DEV02-P1':[('c014',3,1350,1661)],
 'DEV02-P2':[('c014',3,1350,1661)],
 'DEV02-P3':[('c014',3,1350,1661)],
 'DEV02-P4':[('c014',3,1662,1908)],
 'DEV03-P1':[('c035',9,0,90)],
 'DEV03-P2':[('c036',9,91,181)],
 'DEV03-P3':[('c036',9,182,272)],
 'DEV04-P1':[('c044',11,465,618)],
 'DEV04-P2':[('c044',11,465,618),('c044',11,619,753),('c044',11,754,884)],
 'DEV04-P3':[('c044',11,885,960)],
 'DEV04-P4':[('c045',11,961,1192)],
 'DEV05-P1':[('c071',17,283,361)],
 'DEV05-P2':[('c070',16,2248,2483),('c070',17,0,282)],
 'DEV05-P3':[('c070',17,0,282)],
 'DEV06-P1':[('c084',20,1720,1759)],
 'DEV06-P2':[('c084',20,1760,1900)],
 'DEV06-P3':[('c084',20,1901,2061)],
 'DEV06-P4':[('c084',20,1901,2061),('c084',21,0,89)],
 'DEV06-P5':[('c084',21,90,160)],
 'DEV07-P1':[('c061',15,77,434),('c062',15,436,858)],
 'DEV07-P2':[('c062',15,436,858)],
 'DEV07-P3':[('c070',16,2248,2483),('c070',17,0,282),('c071',17,283,361)],
 'DEV07-P4':[('c037',9,733,997),('c037',9,998,1306)],
 'DEV08-P1':[('c035',9,0,90)],
 'DEV08-P2':[('c014',3,1350,1661)],
 'DEV08-P3':[('c035',8,2624,2775)],
 'DEV09-P1':[('c036',9,273,389),('c016',4,376,523),('c016',4,524,809)],
 'DEV09-P2':[], 'DEV09-P3':[],
 'DEV10-P1':[('c016',4,376,523),('c016',4,524,809)],
 'DEV10-P2':[], 'DEV10-P3':[],
}

def audit(rows):
    errors=[]; seen=set(); count=0
    expected={(mode,case['id'],f"DEV{case['id'][-2:]}-P{i}") for mode in ['dense','hybrid'] for case in gold.values() for i in range(1,len(case['mandatory_points'])+1)}
    for row in rows:
        key=(row['mode'],row['case_id'],row['point_id'])
        if key in seen: errors.append([key,'duplicate'])
        seen.add(key)
        if row['gold_point'] != gold[row['case_id']]['mandatory_points'][row['point_index']-1]:errors.append([key,'gold'])
        ctx={c['source_id']:c for c in raw[row['mode'],row['case_id']]['retrieved_contexts']}
        if not row['sources'] and not row.get('na_reason'):errors.append([key,'missing evidence or NA reason'])
        for sp in row['sources']:
            count+=1
            c=ctx.get(sp['source_id']); page,start,end=sp['pdf_page'],sp['start'],sp['end']
            if not c or c['chunk_id']!=sp['chunk_id']:errors.append([key,'source mapping'])
            if not (0<=start<end<=len(pages[page])) or sp['quote']!=pages[page][start:end]:errors.append([key,'page quote'])
            if not c or not any(s['pdf_page']==page and s['page_start_char']<=start<end<=s['page_end_char'] for s in c['source_spans'] if not s.get('is_added_context')):errors.append([key,'context span'])
            if c:
                matched=[s for s in c['source_spans'] if s['pdf_page']==page and s['page_start_char']<=start<end<=s['page_end_char'] and not s.get('is_added_context')]
                if matched:
                    s=matched[0]; a=s['chunk_start_char']+start-s['page_start_char']
                    if c['content'][a:a+end-start]!=sp['quote']:errors.append([key,'context content quote'])
    if seen!=expected:errors.append(['coverage',list(expected-seen),list(seen-expected)])
    return dict(rows=len(rows),unique_keys=len(seen),source_spans=count,errors=errors)

original_audit = audit(original)
assert not original_audit['errors'], original_audit
reviewed=[]; changes=[]
for row in original:
    r=dict(row)
    record=raw[r['mode'],r['case_id']]
    ctx={c['chunk_id']:c for c in record['retrieved_contexts']}
    candidates=[]
    for short,page,start,end in anchors[r['point_id']]:
        chunk=shorts[short]
        assert any(sp['pdf_page']==page and sp['page_start_char']==start and sp['page_end_char']==end and not sp.get('is_added_context') for sp in chunk['source_spans']), (short,page,start,end)
        context=ctx.get(chunk['chunk_id'])
        candidates.append(dict(source_id=context['source_id'] if context else None,chunk_id=chunk['chunk_id'],short_id=short,
             article=chunk['article'],pdf_page=page,start=start,end=end,quote=pages[page][start:end],in_record_context=bool(context)))
    r['gold_sources']=candidates
    r['sources']=[{k:v for k,v in sp.items() if k!='in_record_context'} for sp in candidates if sp['in_record_context']]
    r['raw_answer']=record['answer']
    r['reviewer']='Codex';r['review_date_vietnam']='2026-11-02'
    r['original_grading_reason']=row['reason']
    r['grade_basis']='Giữ nhãn mức đủ ý theo gold của R05; groundedness đánh giá riêng bên dưới.'
    r['na_reason']=None
    if r['point_id']=='DEV07-P4':
        # c038 is a rule for improving an already passed course, not the missing compulsory/elective rule.
        r['claim_support']='unsupported_unconditional_retake_claim'
        r['reason']='Câu trả lời yêu cầu học lại vô điều kiện; c037 khoản1/2 không có trong context. c038 khoản3 nói cải thiện môn đã đạt 5.0–dưới6.5, không chứng minh trường hợp4.5. Giữ nhãn MỘT PHẦN về ý gold, không xác nhận claim faithful.'
    elif not candidates or (r['case_id']=='DEV_08' and r['point_id']=='DEV08-P3' and r['mode']=='dense'):
        r['claim_support']='safe_response_without_separate_positive_evidence'
        r['reason']='Hành vi nêu giới hạn/khuyên liên hệ/từ chối được đối chiếu trực tiếp raw answer; không dựng một đoạn nguồn để chứng minh sự vắng mặt quy định trong cả kho.'
    elif 'SAI' in r['grade']:
        r['claim_support']='contradicted_by_context'
        r['reason']='D+ thuộc5.0–5.4 trong bảng c062; claim D+ trở xuống đều dưới5.0 trái context. Giữ SAI.'
    elif not r['sources']:
        r['claim_support']='missing_retrieved_gold_evidence'
        r['reason']='Các căn cứ gold được lưu riêng nhưng không có trong context của record; không gán source ID cho chúng và không đổ lỗi generation nếu thiếu retrieval.'
    elif 'THIẾU' in r['grade']:
        r['claim_support']='generation_omission_with_retrieved_evidence'
        r['reason']='Context chứa các spans hỗ trợ ý gold nhưng raw answer bỏ sót ý này.'
    else:
        r['claim_support']='supported_by_selected_context_spans'
        r['reason']='Đã đọc các spans hỗ trợ đủ các thành phần của ý gold, kể cả nhánh điều kiện hoặc phần nối trang; source ID lấy theo đúng record.'
    if not r['sources']:
        r['na_reason']=r['reason']
    old={(sp['source_id'],sp['chunk_id'],sp['pdf_page'],sp['start'],sp['end']) for sp in row['sources']}
    new={(sp['source_id'],sp['chunk_id'],sp['pdf_page'],sp['start'],sp['end']) for sp in r['sources']}
    if old!=new:
        changes.append(dict(mode=r['mode'],case_id=r['case_id'],point_id=r['point_id'],old_spans=sorted(old),reviewed_spans=sorted(new),claim_support=r['claim_support']))
    reviewed.append(r)

checked=audit(reviewed)
assert not checked['errors'], checked
out=RESULTS/'EVIDENCE_DEV10_TASK05_CODEX_VERIFIED.jsonl'
out.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in reviewed),encoding='utf-8')
labels=collections.Counter((r['mode'],r['grade']) for r in reviewed)
support=collections.Counter(r['claim_support'] for r in reviewed)
hashfiles=[SRC/'data/QD580_CHUNKS.jsonl',SRC/'data/QD580_MANIFEST.json',PAGES,SRC/'evaluation/DEV_10_CAU_QD580.jsonl',RESULTS/'DNC_RAG_AB_DEV10_TASK05.jsonl',RESULTS/'DNC_RAG_AB_DEV10_TASK05.csv',RESULTS/'EVIDENCE_DEV10_TASK05_R05.jsonl']
summary=dict(review_date_vietnam='2026-11-02',reviewed_commit='23f240f6a5d5d52ab8b67fa82e741d626f6b0bd9',
             original_sidecar_structural_audit=original_audit,codex_sidecar_structural_audit=checked,
             amended_source_rows=len(changes),changes=changes,claim_support_counts=dict(support),
             original_grades_preserved=True,label_counts={str(k):v for k,v in labels.items()},
             validation_scope='Exact rows, gold, source mappings, page/context quotes and spans. Semantic anchors read by Codex; not a claim of perfect LLM output.',
             hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in hashfiles},
             script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),review_artifacts_uncommitted=True)
(RESULTS/'KIEM_TRA_DOC_LAP_TASK05_R05.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:summary[k] for k in ['original_sidecar_structural_audit','codex_sidecar_structural_audit','amended_source_rows','claim_support_counts']},ensure_ascii=False,indent=2))
