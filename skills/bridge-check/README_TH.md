# bridge-check — คู่มือติดตั้งและใช้งาน (ภาษาไทย)

คู่มือฉบับไทยของ skill `bridge-check` (ตัวเปิดประตูสะพาน + กู้กระแสข้อมูลกลับ)
อ้างอิงตัวจริง: `SKILL.md` ในโฟลเดอร์เดียวกันนี้

## หน้าที่โดยย่อ
- กล่องจดหมายกลาง (central event inbox) เป็นทางเข้าเดียวของระบบ
- เมื่อ "สะพาน" ขาด (bridge down) ข้อมูลจากภายนอกจะเข้าไม่ถึงแต่ละช่อง
  skill นี้เปิดประตูใหม่แล้วดันของที่ค้าง (backlog) กลับเข้าช่องทุกใบ

## ของที่ต้องมีบนเครื่อง (ไฟล์จริงทั้งหมด)
| ไฟล์ | หน้าที่ |
|---|---|
| `/var/minis/shared/tools/bridge-check/bridge_open_event.sh` | สคริปต์หลัก — ตัวเดียวที่ถูกรัน |
| `/var/minis/shared/tools/bridge-check/bin/` | ตัวรันจริง (mesh_guard.sh, mesh_watch.py ฯลฯ) |
| `/var/minis/shared/tools/bridge-check/runtime/` | pid / hb / log / lock ของการ heal |
| `/var/minis/skills/bridge-check/SKILL.md` | ตัวที่แอปโหลด (มิเรอร์ของ SKILL.md ในโฟลเดอร์นี้) |

## การติดตั้ง Shortcut บน iPhone
1. นำเข้า `MinisBridgeHeal-ntfy` (ครั้งแรก iOS จะถาม Allow/Import Anyway — กด Allow)
2. ตั้ง Automation: เกิดจาก **notification ของ ntfy** เท่านั้น (topic `peach-events`,
   ข้อความรูปแบบ `[WAKE:<scope>]` / `VM WAKE`) — ไม่ใช่ "เปิดแอป"
3. Shortcut ส่งข้อความ `/bridge-check` เข้าช่อง "เวลา (scheduled)" เท่านั้น
   ห้ามใส่พาธสคริปต์หรือตรรกะใน Shortcut — ตัวรันจริงอยู่ที่ `bridge_open_event.sh`

## วิธีเรียกใช้
- อัตโนมัติ: ntfy แจ้งเตือน → Automation ยิง `/bridge-check` เข้าช่อง scheduled
- มือ: พิมพ์ "เช็คสะพาน" หรือ "bridge check" ในแชท

## สคริปต์ทำอะไร (เรียงตามลำดับ)
1. ล็อก 180 วินาที (กันซ้อน)
2. เช็ค `mesh_watch.pid` ยังมีชีวิต + heartbeat อายุ < 90 วิ
   → ถ้าปกติ ตอบ `bridge healthy; no action` แล้วออก (exit 0)
3. ถ้าตาย/ค้าง: รัน `bin/mesh_guard.sh` เพื่อ heal, บันทึก log เป็น
   `HEALED:` หรือ `FAILED rc=`, exit ตามผล guard
- ห้ามรันจาก shell startup (กัน mesh reader ซ้อนกัน) — รันเมื่อถูกเรียกชัดเจนเท่านั้น

## ตรวจสุขภาพ (รันตามลำดับ อ้างผลจริงทุกบรรทัด)
1. `minis-mcp-cli call vm-hq-gate vm_health` — hq-core / nginx
2. `curl -s http://127.0.0.1:4300/api/health` (ควรได้ ws:true, firestore:true)
   และ `curl -s http://127.0.0.1:4301/health` (ควรได้ ok)
3. นับ backlog ใน Firestore `webhookInbox` สถานะ new — ถ้า >0 และสะพานลง = ประตูปิด
4. ทดสอบ SSE ingest → ควรได้ 201 ถ้าไม่ได้ให้ resend คิวค้าง
5. `sh /var/minis/shared/tools/bridge-check/bridge_open_event.sh` → ตอนปกติต้องได้
   `bridge healthy; no action`

## เปิดประตูเมื่อสะพานลง
1. ยิง SSE ingest ซ้ำ (ประตูหลัก ไม่ต้องมี tunnel)
2. สร้าง tunnel ใหม่: `OM_SSH_NOMUX=1 om-ssh -t auto -L 14301:127.0.0.1:4301 -N &`
3. รีสตาร์ต `mesh_guard.sh` ถ้า pid ตาย
4. รัน `mesh_sweep.js` ดัน backlog กลับช่อง — อ้าง `moved=N` เป็นหลักฐานว่าไหลแล้ว
5. นับ backlog เหลือ ต้องเป็น 0 หรือเหลือแต่ skipped
6. รายงานสถานะก่อน/หลัง + จำนวน moved ให้พี่พีช

## กฎวินัย
- อ้างหลักฐานจริงเสมอ (บรรทัด health, จำนวน backlog, บรรทัด moved/skipped)
  ห้ามพูดว่า "สะพานโอเค" โดยไม่มีบรรทัดพิสูจน์
- ประตูหลัก = SSE ingest (proxyToVm) ใช้ได้แม้ Tailscale ปิด
- หาก VM ไม่ตอบเลย ให้แจ้งช่อง code (ปั้นแป้ง) ตาม WO escalation
