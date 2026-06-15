# DAX Measures

## AOV (Average Order Value)

```DAX
Total GMV =
SUM(v_monthly_aov[monthly_gmv])

Total Orders =
SUM(v_monthly_aov[total_orders])

AOV =
DIVIDE(
    [Total GMV],
    [Total Orders]
)
```

**เหตุผลที่ใช้ DAX**

ใช้ DAX เพื่อคำนวณ Average Order Value (AOV) ภายใน Power BI จากยอดขายรวม (GMV) และจำนวนคำสั่งซื้อ (Orders) แทนการดึงค่า AOV ที่คำนวณสำเร็จจาก Data Mart โดยตรง ทำให้สามารถปรับเปลี่ยนสูตรหรือเงื่อนไขทางธุรกิจได้ง่ายในชั้น Business Intelligence โดยไม่ต้องแก้ไข SQL ใน BigQuery

---

## On-time Delivery Rate %

```DAX
On-time Delivery Rate % =
DIVIDE(
    SUM(v_monthly_on_time_delivery_rate[on_time_orders]),
    SUM(v_monthly_on_time_delivery_rate[delivered_orders])
)
```

**เหตุผลที่ใช้ DAX**

ใช้ DAX เพื่อคำนวณอัตราการจัดส่งตรงเวลาจากจำนวนออเดอร์ที่ส่งตรงเวลาและจำนวนออเดอร์ที่จัดส่งทั้งหมดภายใน Power BI โดยตรง ช่วยให้ตรรกะการคำนวณ KPI อยู่ในชั้น BI และสามารถนำไปใช้กับ Visual หรือรายงานอื่น ๆ ได้สะดวก โดยไม่จำเป็นต้องสร้าง Metric ใหม่ใน Data Warehouse
