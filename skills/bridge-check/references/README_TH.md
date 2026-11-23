# bridge-check — คู่มือใช้งานภาษาไทย

`bridge-check` คือกลไกเปิดหรือกู้เส้นทาง app → VM เพื่อให้ event ที่เข้าคิวแล้วไหลกลับไปยัง lane ที่ถูกต้อง ไม่ใช่ตัวนับคิว ไม่ใช่ shell และไม่ใช่เจ้าของ work-order state

## ขอบเขต

- เรียกใช้ registered bridge-health/recovery capability
- เปิดหรือ heal WS/tunnel/mesh watcher ตาม deployment ที่ได้รับอนุญาต
- รายงาน verdict สด: `bridge healthy; no action`, `HEALED:` หรือ `FAILED rc=`
- หากมีหลักฐานจาก opener ให้รายงาน `moved=N`

เส้นทางจริงและตำแหน่งไฟล์เป็น runtime facts ไม่ควรเดาจากเอกสารนี้ขณะสถานะยังเป็น `runtime verification pending` ห้ามใส่ path, host, token หรือ SSH target ลงใน Shortcut เอง

## วิธีเรียก

- ntfy/Shortcut ส่ง wake message ไปยัง scheduled lane ตาม configuration ที่ผู้ใช้ตั้งไว้
- ผู้ใช้พิมพ์ `เช็คสะพาน`, `ต่อสะพาน` หรือ `bridge check`
- Agent เรียก skill นี้หนึ่งครั้ง แล้วรายงานผลของ opener ตามจริง

## ลำดับปฏิบัติ

1. Resolve capability จาก `registry/transports.json`
2. เรียก bridge opener ที่ runtime ลงทะเบียนไว้หนึ่งครั้ง
3. ไม่ loop-retry หากล้มเหลว ให้ส่งบรรทัด `FAILED rc=` ตามจริง
4. ไม่เขียน pad, board หรือ work-order state จาก bridge-check
5. หากต้องทำงานหรือปิดงาน ให้ใช้ `wo-loop` แยกต่างหาก

## เส้นทางและ authority

- WS เป็น primary สำหรับ lifecycle และคำสั่งเล็ก/structured
- Tailscale direct SSH เป็น primary สำหรับ bulk/large/raw/interactive เมื่อ registry เลือก
- IAP เป็น compatibility-only
- `vm-hq-gate` เป็น typed VM gateway
- `minis-tools` เป็น device/WS adapter
- VM เป็นเจ้าของ durable state; device เป็น UI/transport adapter

## หลักฐาน

ห้ามรายงานว่า bridge ปกติโดยไม่มี output สดจาก opener หรือ registered health capability และห้ามแก้ไข Shortcut อัตโนมัติ—iOS Shortcut เป็นของผู้ใช้
