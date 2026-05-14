# 🛰️ Remote Sensing Land Classification

**Interactive Streamlit web application for satellite image land cover classification using Machine Learning**

## 📋 المتطلبات

- Python 3.10+
- pip (مدير الحزم)

## 🚀 التثبيت والتشغيل

### 1. استنساخ المشروع (أو تنزيل الملفات)
```bash
git clone https://github.com/mo7sen137/Remote_Sensing.git
cd Remote_Sensing
```

### 2. إنشاء بيئة افتراضية (Virtual Environment)
```bash
python -m venv venv
```

#### تفعيل البيئة:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. تثبيت الحزم
```bash
pip install -r requirements.txt
```

### 4. تشغيل التطبيق
```bash
streamlit run app/main.py
```

أو استخدم الـ script المرفق:
```bash
bash run_app.sh
```

التطبيق سيفتح تلقائياً في المتصفح على: `http://localhost:8501`

---

## 📂 بنية المشروع

```
Remote_Sensing/
├── app/
│   ├── __init__.py           # تهيئة حزمة التطبيق
│   ├── main.py               # التطبيق الرئيسي (Streamlit)
│   ├── callbacks.py          # معالجات الأحداث
│   └── components.py         # مكونات الواجهة
├── src/
│   ├── __init__.py          # تهيئة حزمة الكود
│   ├── model_trainer.py     # تدريب النماذج
│   ├── feature_extractor.py # استخراج الميزات
│   ├── utils.py             # دوال مساعدة
│   ├── preprocessor.py      # معالجة البيانات
│   ├── classifier.py        # التصنيف
│   └── postprocessor.py     # معالجة ما بعد التصنيف
├── config.py                # الإعدادات
├── requirements.txt         # الحزم المطلوبة
├── run_app.sh              # سكريبت التشغيل
├── sample_bands.csv        # عينة بيانات (Bands)
├── sample_roi.csv          # عينة بيانات تدريب (ROI)
└── README.md               # هذا الملف
```

---

## 🎯 استخدام التطبيق

### الخطوة 1: رفع البيانات (Upload Data)
- **Bands CSV:** ملف CSV يحتوي على 7 أعمدة (B1-B7) للنطاقات الطيفية
- **Metadata BIN:** ملف بيانات المعالجة الإشعاعية
- عينات موجودة: `sample_bands.csv` و `sample_roi.csv`

### الخطوة 2: المعاينة (Preview)
- عرض البيانات المرفوعة
- معلومات الفهارس الطيفية (NDVI, NDWI, NDBI)

### الخطوة 3: التصنيف (Classification)
- اختر نموذج ML (Random Forest موصى به)
- رفع ملف البيانات التدريبية (ROI)
- اضغط "Execute Classification"

### الخطوة 4: النتائج (Results)
- عرض خريطة التصنيف بـ 4 فئات:
  - 🔵 Water (ماء)
  - 🟢 Vegetation (نبات)
  - 🔴 Urban (عمران)
  - 🟠 Desert (صحراء)
- تحميل النتائج (PNG, Excel, TXT)

---

## 📊 الميزات

### معالجة البيانات:
- ✅ معايرة إشعاعية (Radiometric Calibration)
- ✅ حساب الفهارس الطيفية (NDVI, NDWI, NDBI)
- ✅ معالجة البيانات المفقودة

### نماذج التصنيف:
- ✅ Random Forest (الموصى به)
- ✅ Support Vector Machine (SVM)
- ✅ K-Nearest Neighbors (KNN)
- ✅ Decision Tree
- ✅ Neural Network (MLP)

### التصور والتصدير:
- ✅ خريطة ملونة احترافية
- ✅ إحصائيات دقيقة (المساحة والنسبة المئوية)
- ✅ تصدير PNG, Excel, TXT
- ✅ رسوم بيانية للدقة

### تحسينات الأداء:
- ✅ معالجة بالأجزاء (Chunking) - توفير الذاكرة
- ✅ تخزين مؤقت (Caching) - تسريع إعادة التشغيل
- ✅ ترتيب reshape صحيح (MATLAB compatible)
- ✅ فحوصات شاملة لصحة البيانات

---

## 🔧 المتطلبات البرمجية

| الحزمة | الإصدار | الغرض |
|--------|---------|-------|
| streamlit | ≥1.28.0 | تطبيق الويب |
| numpy | ≥1.26.0 | معالجة المصفوفات |
| pandas | ≥2.0.0 | معالجة البيانات |
| scikit-learn | ≥1.3.0 | نماذج ML |
| matplotlib | ≥3.7.0 | رسم الرسوم البيانية |
| pillow | ≥10.0.0 | معالجة الصور |
| openpyxl | ≥3.1.0 | تصدير Excel |

انظر `requirements.txt` لقائمة كاملة.

---

## 📝 ملفات البيانات النموذجية

### sample_bands.csv
```csv
B1,B2,B3,B4,B5,B6,B7
5000,4800,4600,4400,6500,4000,3800
5100,4900,4700,4500,6600,4100,3900
...
```

### sample_roi.csv
```csv
B1,B2,B3,B4,B5,B6,B7,Class_Label
3000,2800,2600,2400,5000,2500,1800,1
3100,2900,2700,2500,5100,2600,1900,2
...
```

---

## 🛠️ استكشاف الأخطاء

### خطأ: "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### خطأ: "No columns to parse from file"
تأكد من أن ملف CSV يحتوي على:
- الأعمدة الصحيحة (B1-B7 و Class_Label)
- على الأقل صف واحد من البيانات

### الخريطة تظهر بدون تفاصيل؟
تم تصحيح ترتيب reshape ليطابق MATLAB - يجب أن تظهر الآن بشكل احترافي.

---

## 📞 المساعدة والدعم

- اطلع على التوثيق في الملفات
- تأكد من تثبيت جميع الحزم
- استخدم عينات البيانات المرفقة للاختبار الأول

---

## 📄 الترخيص

هذا المشروع مفتوح المصدر.

---

**آخر تحديث:** مايو 2026
**الإصدار:** 1.0.0
