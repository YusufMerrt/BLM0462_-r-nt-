# -*- coding: utf-8 -*-
"""
Örüntü Tanımaya Giriş — Vize Soru Bankası PDF Üreticisi
"""

import json
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors

# ---------- Turkish font ----------
FONT_REG = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("ArialU", FONT_REG))

# ---------- Styles ----------
styles = getSampleStyleSheet()
base = ParagraphStyle(
    "Base", parent=styles["Normal"],
    fontName="ArialU", fontSize=10.5, leading=14,
    alignment=TA_JUSTIFY, spaceAfter=4,
)
title_style = ParagraphStyle(
    "Title", parent=base, fontName="ArialU", fontSize=22, leading=28,
    alignment=TA_CENTER, spaceAfter=10, textColor=colors.HexColor("#1a365d"),
)
subtitle_style = ParagraphStyle(
    "SubTitle", parent=base, fontSize=12, leading=16,
    alignment=TA_CENTER, spaceAfter=6, textColor=colors.HexColor("#2d3748"),
)
h1_style = ParagraphStyle(
    "H1", parent=base, fontSize=16, leading=20, alignment=TA_LEFT,
    textColor=colors.white, backColor=colors.HexColor("#2b6cb0"),
    borderPadding=6, spaceBefore=16, spaceAfter=10,
)
h2_style = ParagraphStyle(
    "H2", parent=base, fontSize=13, leading=17, alignment=TA_LEFT,
    textColor=colors.HexColor("#2b6cb0"), spaceBefore=10, spaceAfter=6,
)
q_style = ParagraphStyle(
    "Q", parent=base, fontSize=10.5, leading=14, leftIndent=0, spaceAfter=2,
)
opt_style = ParagraphStyle(
    "Opt", parent=base, fontSize=10.3, leading=13, leftIndent=18, spaceAfter=1,
)
note_style = ParagraphStyle(
    "Note", parent=base, fontSize=9.5, leading=12, textColor=colors.HexColor("#4a5568"),
    alignment=TA_LEFT,
)
ans_style = ParagraphStyle(
    "Ans", parent=base, fontSize=10, leading=13, alignment=TA_LEFT,
)

story = []


def h1(text):
    story.append(Paragraph(text, h1_style))


def h2(text):
    story.append(Paragraph(text, h2_style))


def note(text):
    story.append(Paragraph(text, note_style))
    story.append(Spacer(1, 4))


def mcq(n, q, options, answer, explanation=None):
    """n: numara, q: soru, options: list of 4-5 string, answer: index (0-based)"""
    letters = ["A", "B", "C", "D", "E"]
    block = [Paragraph(f"<b>{n}.</b> {q}", q_style)]
    for i, op in enumerate(options):
        block.append(Paragraph(f"{letters[i]}) {op}", opt_style))
    block.append(Spacer(1, 5))
    story.append(KeepTogether(block))
    quiz_mcq_data.append({
        "id": n,
        "question": q,
        "options": options,
        "correctIndex": answer,
        "explanation": explanation or "",
    })
    return (n, letters[answer], explanation or "")


def fib(n, sentence, answer, explanation=None):
    """Fill-in-the-blank"""
    block = [Paragraph(f"<b>{n}.</b> {sentence}", q_style), Spacer(1, 6)]
    story.append(KeepTogether(block))
    # Birden fazla boşluk için cevaplar ";" ile ayrılır
    parts = [p.strip() for p in answer.split(";")]
    quiz_fib_data.append({
        "id": n,
        "sentence": sentence,
        "answers": parts,
        "explanation": explanation or "",
    })
    return (n, answer, explanation or "")


# ---------- COVER ----------
story.append(Spacer(1, 2 * cm))
story.append(Paragraph("ÖRÜNTÜ TANIMAYA GİRİŞ", title_style))
story.append(Paragraph("Vize Soru Bankası", subtitle_style))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    "BLM0462 — Örüntü Tanıma (Pattern Recognition)", subtitle_style))
story.append(Paragraph("2025–2026 Bahar Dönemi", subtitle_style))
story.append(Spacer(1, 1 * cm))
story.append(Paragraph(
    "<b>Kapsam:</b> Hafta 1 – Giriş · Bölüm 2 Bayesian Karar Teorisi · "
    "Bölüm 3 Parametrik Kestirim (MLE / Bayes / EM) · "
    "Ünite 4 Parzen Pencereleri · Ünite 4 (k-NN) · "
    "Bayesian Belief Networks · Hidden Markov Model",
    base))
story.append(Spacer(1, 0.8 * cm))
story.append(Paragraph(
    "Bu çalışma kitapçığı ders slaytlarınızdan türetilen <b>kavramsal</b> "
    "çoktan seçmeli ve boşluk doldurmalı sorulardan oluşmaktadır. "
    "Sayısal hesaplama sorusu <b>yoktur</b>. Her bölüm sonunda cevap "
    "anahtarı bulunmaktadır.",
    base))
story.append(PageBreak())

answers_mcq = []  # (n, letter, explanation)
answers_fib = []  # (n, answer, explanation)

# Web quiz için tam soru verisi (JSON dışa aktarımında kullanılır)
quiz_mcq_data = []
quiz_fib_data = []

# =====================================================================
# BÖLÜM 1 — HAFTA 1: ÖRÜNTÜ TANIMAYA GİRİŞ
# =====================================================================
h1("BÖLÜM 1 — Hafta 1: Örüntü Tanımaya Giriş")
h2("A. Çoktan Seçmeli Sorular")

N = 0


def _next():
    global N
    N += 1
    return N


answers_mcq.append(mcq(_next(),
    "Aşağıdakilerden hangisi örüntü tanımanın (pattern recognition) en temel tanımıdır?",
    ["Ham veriyi (görüntü, ses, metin) alıp bir kategoriye atama ve buna göre eylem üretme süreci",
     "Bir veritabanında arama yapma süreci",
     "Verilerin görselleştirilmesi",
     "Yalnızca istatistiksel testler yürütmek",
     "Programlama dili tasarlamak"],
    0, "Örüntü tanıma ham veriyi karara dönüştürme sürecidir."))

answers_mcq.append(mcq(_next(),
    "Balık sınıflandırma sisteminde tipik işlem hattı (pipeline) hangi sırayla ilerler?",
    ["Sınıflandırma → Özellik çıkarımı → Ön işleme → Algılama",
     "Algılama → Ön işleme → Bölütleme → Özellik çıkarımı → Sınıflandırma → Son-işleme",
     "Ön işleme → Algılama → Son-işleme → Sınıflandırma",
     "Bölütleme → Sınıflandırma → Algılama → Ön işleme",
     "Sınıflandırma → Algılama → Özellik çıkarımı"],
    1))

answers_mcq.append(mcq(_next(),
    "Balık örneğinde “uzunluk” tek özelliği ile sınıflandırma neden yeterli değildir?",
    ["Uzunluk ölçülemeyecek kadar küçüktür",
     "Uzunluk değeri zamanla değişir",
     "İki sınıfın uzunluk dağılımları birbirine çakışır ve ayırıcı olarak zayıftır",
     "Uzunluk yalnızca somon için tanımlıdır",
     "Uzunluk sadece görüntüden ölçülemez"],
    2))

answers_mcq.append(mcq(_next(),
    "Gürültü (noise) için aşağıdakilerden hangisi doğrudur?",
    ["Modelin kendisinin bir parçasıdır",
     "Gerçek modele ait olmayan, rastlantısal/sensörel değişkenliktir",
     "Her zaman tamamen ortadan kaldırılabilir",
     "Yalnızca görüntü verisinde görülür",
     "Karar sınırının konumunu hiçbir şekilde etkilemez"],
    1))

answers_mcq.append(mcq(_next(),
    "Aşırı öğrenme (overfitting) kavramının en doğru tanımı aşağıdakilerden hangisidir?",
    ["Modelin eğitim verisini ezberleyip yeni (görülmemiş) veride kötü performans göstermesi",
     "Modelin hem eğitim hem test verisinde yüksek hata vermesi",
     "Modelin çok hızlı eğitilmesi",
     "Modelin çok yavaş yakınsaması",
     "Modelin yetersiz eğitilmesi"],
    0))

answers_mcq.append(mcq(_next(),
    "Aşağıdakilerden hangisi aşırı öğrenmeye karşı alınabilecek etkili bir önlemdir?",
    ["Modeli daha karmaşık hale getirmek",
     "Daha fazla veri toplamak, daha basit model kullanmak veya düzenlileştirme (regularization) uygulamak",
     "Özellik çıkarımını tamamen kaldırmak",
     "Eğitim verisini küçültmek",
     "Test verisini eğitime dâhil etmek"],
    1))

answers_mcq.append(mcq(_next(),
    "Karar sınırının (decision boundary) konumu yalnızca doğruluk oranına göre değil, aynı zamanda neye göre belirlenir?",
    ["Karar hatalarının maliyeti (cost) ve risklere göre",
     "Algoritmanın çalışma hızına göre",
     "Veri setinin boyutuna göre",
     "Programlama diline göre",
     "Sensörün markasına göre"],
    0))

answers_mcq.append(mcq(_next(),
    "Denetimli öğrenme (supervised learning) ile ilgili aşağıdakilerden hangisi doğrudur?",
    ["Girdi verileri etiketsizdir, sistem doğal gruplar bulur",
     "Her örnek için sınıf etiketi veya maliyet bulunur, amaç toplam hatayı minimize etmektir",
     "Yalnızca ödül/ceza sinyali ile çalışır",
     "Yalnızca görüntü verisi için kullanılabilir",
     "Parametreleri sabittir, öğrenme yoktur"],
    1))

answers_mcq.append(mcq(_next(),
    "Denetimsiz öğrenme (unsupervised learning) tipik olarak hangi amaçla kullanılır?",
    ["Etiketli veri ile sınıflandırma",
     "Ödül sinyali ile politika öğrenme",
     "Etiketsiz veride doğal grupları (kümeleri) keşfetmek",
     "Maliyet fonksiyonunu doğrudan minimize etmek",
     "Regresyon fonksiyonu oturtmak"],
    2))

answers_mcq.append(mcq(_next(),
    "Pekiştirmeli öğrenmede (reinforcement learning) öğrenme sinyali nasıldır?",
    ["Doğru etiket eğitmen tarafından verilir",
     "Yalnızca doğru/yanlış veya skaler bir ödül verilir",
     "Veri etiketsizdir ve ödül yoktur",
     "Doğrudan karar sınırı verilir",
     "Tüm parametreler baştan sabittir"],
    1))

answers_mcq.append(mcq(_next(),
    "Değişmezlik (invariance) kavramı bir örüntü tanıma sisteminde ne anlama gelir?",
    ["Sınıflandırıcı kategoriye etkisi olmayan dönüşümlere (öteleme, döndürme vb.) karşı duyarsız olmalıdır",
     "Özellik sayısı zaman içinde değişmemelidir",
     "Sınıf etiketleri asla güncellenmemelidir",
     "Eğitim verisi asla değişmemelidir",
     "Gürültü tamamen sıfır olmalıdır"],
    0))

answers_mcq.append(mcq(_next(),
    "Bağlam (context) kullanmak neden işe yarayabilir ama aynı zamanda risklidir?",
    ["Bağlam her zaman hatalıdır",
     "Bağlam veriden daha önemsizdir",
     "Doğru bağlam belirsiz örneği düzeltebilir; yanlış bağlam varsayımı ise hatayı artırabilir",
     "Bağlam yalnızca görüntü işlemede tanımlıdır",
     "Bağlam karar sınırını hareketsiz tutar"],
    2))

answers_mcq.append(mcq(_next(),
    "Bölütleme (segmentation) problemi için “tavuk-yumurta sorunu” ifadesi neyi anlatır?",
    ["Veri hiç yoksa bölütleme yapılamaz",
     "Tanımadan bölütlemek zor, bölütlemeden tanımak zor olduğundan iki süreç birbirine bağımlıdır",
     "Segmentation her zaman otomatiktir",
     "Bölütleme yalnızca renkli görüntülerde çalışır",
     "Bölütleme maliyeti sıfırdır"],
    1))

answers_mcq.append(mcq(_next(),
    "Eksik özellikler (missing features) için hangi ifade yanlıştır?",
    ["Sensör arızası, veri kaybı veya eksik test sonuçları gerçek hayatta sık karşılaşılan nedenlerdir",
     "Eksik değeri ortalama ile doldurmak her zaman optimal bir çözümdür",
     "Eksik bilgiyle karar verebilen yöntemler ve eğitim stratejileri gerekir",
     "Bir özellik, örneğin occlusion (üst üste gelme) nedeniyle ölçülemeyebilir",
     "Eksik özellik sınıflandırma performansını etkileyebilir"],
    1,
    "Ortalamaya göre doldurma bir çözüm olsa da optimal değildir."))

answers_mcq.append(mcq(_next(),
    "Örüntü tanıma (pattern recognition) ile örüntü sınıflandırma (pattern classification) arasındaki ilişki en iyi nasıl tanımlanır?",
    ["İkisi birbirinden tamamen bağımsızdır",
     "Sınıflandırma, tanıma için gerekli olan karar adımıdır; tanıma süreci algılama, ön işleme, özellik çıkarımı ve sınıflandırmayı birlikte içerir",
     "Sınıflandırma yalnızca tıbbi teşhiste kullanılır",
     "Tanıma yalnızca ses verisi için tanımlıdır",
     "Tanıma ve sınıflandırma her zaman özdeştir"],
    1))

answers_mcq.append(mcq(_next(),
    "Aşağıdakilerden hangisi örüntü tanımanın pratik uygulama alanlarından <b>değildir</b>?",
    ["Yüz tanıma", "Spam filtresi", "Tıbbi teşhis", "Derleyici (compiler) tasarımı", "DNA dizi tanıma"],
    3))

answers_mcq.append(mcq(_next(),
    "Maliyet/risk ayarlaması karar eşiğini nasıl kaydırır? (Balık örneği)",
    ["Eşik daima sabit kalır",
     "Eğer levreği somon sanmak daha pahalıysa eşik, somon kararını daha az olası kılacak şekilde kaydırılır",
     "Eşik daima minimum olasılığa çekilir",
     "Maliyetin etkisi yoktur",
     "Eşik rastgele belirlenir"],
    1))

answers_mcq.append(mcq(_next(),
    "Genelleme (generalization) kavramı için aşağıdakilerden hangisi doğrudur?",
    ["Eğitim verisindeki hatayı sıfırlamaktır",
     "Görülmemiş (yeni) veride doğru karar verebilme yeteneğidir",
     "Modelin karmaşıklığını artırmaktır",
     "Veri önişlemeyi atlamaktır",
     "Yalnızca etiketsiz verilerde geçerlidir"],
    1))

answers_mcq.append(mcq(_next(),
    "Makine algısı (machine perception) kavramının temel amacı nedir?",
    ["İnsan algısından tamamen bağımsız sistemler tasarlamak",
     "İnsan algısına benzer şekilde örüntüleri otomatik tanımak",
     "Sadece sayısal hesaplamalar yapmak",
     "Verileri yalnızca sıkıştırmak",
     "Doğal dilde metin üretmek"],
    1))

answers_mcq.append(mcq(_next(),
    "Aşağıdaki öğrenme türü eşleştirmelerinden hangisi <b>yanlıştır</b>?",
    ["Denetimli öğrenme — spam filtresi",
     "Denetimsiz öğrenme — müşteri segmentasyonu",
     "Pekiştirmeli öğrenme — robot navigasyonu",
     "Denetimsiz öğrenme — etiketli yüz tanıma",
     "Pekiştirmeli öğrenme — ödül sinyali tabanlı"],
    3))

h2("B. Boşluk Doldurmalı Sorular")

F = 0


def _fnext():
    global F
    F += 1
    return F


answers_fib.append(fib(_fnext(),
    "Örüntü tanıma sisteminin standart boru hattı (pipeline) şu sırayla ilerler: algılama → __________ → bölütleme → __________ → sınıflandırma → son-işleme.",
    "ön işleme (preprocessing); özellik çıkarımı (feature extraction)"))

answers_fib.append(fib(_fnext(),
    "Karar sınırı (decision boundary) tek özellikte bir __________, iki özellikte bir __________, üç özellikte bir __________ ile temsil edilir.",
    "nokta; eğri/doğru; yüzey"))

answers_fib.append(fib(_fnext(),
    "Modelin eğitim verisini ezberleyip yeni verilerde kötü sonuç vermesine __________ denir; buna karşı amaç __________ (yeni verilerde başarı) elde etmektir.",
    "aşırı öğrenme (overfitting); genelleme (generalization)"))

answers_fib.append(fib(_fnext(),
    "Etiketli veri ile öğrenmeye __________; etiketsiz veride doğal grupları bulmaya __________; ödül sinyali ile öğrenmeye ise __________ öğrenme denir.",
    "denetimli (supervised); denetimsiz (unsupervised); pekiştirmeli (reinforcement)"))

answers_fib.append(fib(_fnext(),
    "Bir sınıflandırıcının kategoriye etkisi olmayan dönüşümlere (öteleme, döndürme vb.) karşı duyarsız olmasına __________ özelliği denir.",
    "değişmezlik (invariance)"))

answers_fib.append(fib(_fnext(),
    "Hedef örüntü dışındaki, girdiye bağlı ek bilgiye __________ denir; bu bilgi doğru kullanılırsa hatayı azaltır.",
    "bağlam (context)"))

answers_fib.append(fib(_fnext(),
    "Ham veriyi daha düşük boyutlu, ayırt edici bir temsile dönüştürme işlemine __________ denir.",
    "özellik çıkarımı (feature extraction)"))

answers_fib.append(fib(_fnext(),
    "Gürültü özellik değerlerini kaydırdığından, __________ sınırına yakın örneklerde sınıflandırma hatası artar.",
    "karar (decision)"))

answers_fib.append(fib(_fnext(),
    "Bir örnekte birden fazla özellik bir araya getirilerek oluşturulan vektöre __________ denir; bu vektörün yaşadığı uzaya ise __________ denir.",
    "özellik vektörü (feature vector); özellik uzayı (feature space)"))

answers_fib.append(fib(_fnext(),
    "Çok karmaşık bir karar sınırı eğitim verisini ezberleyebilir; ancak gerçek hedef __________ (yeni veri başarısı) olduğundan model __________ (basitlik) ve doğruluk arasında dengelenmelidir.",
    "genelleme; karmaşıklık"))

# =====================================================================
# BÖLÜM 2 — BAYESIAN KARAR TEORİSİ
# =====================================================================
story.append(PageBreak())
h1("BÖLÜM 2 — Bayesian Karar Teorisi")
h2("A. Çoktan Seçmeli Sorular")

answers_mcq.append(mcq(_next(),
    "Bayesian karar teorisinin temel varsayımlarından hangisi <b>yanlıştır</b>?",
    ["Karar problemi olasılıksal terimlerle ifade edilebilmektedir",
     "Tüm ilgili olasılık dağılımları bilinmektedir",
     "Hatalı sınıflandırmaların maliyeti sayısal olarak tanımlanabilir",
     "Dağılımların hiçbiri bilinmek zorunda değildir",
     "Olasılıklar (önsel, olabilirlik) birleştirilerek karar verilir"],
    3))

answers_mcq.append(mcq(_next(),
    "Bayes formülünde <i>sonsal (posterior)</i> olasılık hangisidir?",
    ["p(x|ω)",
     "P(ω)",
     "P(ω|x) — x ölçüldükten sonra sınıf olasılığı",
     "p(x) — kanıt (evidence)",
     "λ(α|ω) — kayıp fonksiyonu"],
    2))

answers_mcq.append(mcq(_next(),
    "Bayes formülünde kanıt (evidence) terimi p(x) neden karara doğrudan etki etmez?",
    ["Her zaman 1’e eşittir",
     "Kararı her iki sınıf için de aynı şekilde bölerek sadeleşir",
     "Sıfıra eşittir",
     "Yalnızca önsel olasılığa eşittir",
     "Her zaman Gauss olduğu varsayılır"],
    1))

answers_mcq.append(mcq(_next(),
    "Bayes karar kuralına göre iki sınıflı problemde ω1 seçilir, eğer:",
    ["P(ω1) > P(ω2)",
     "p(x|ω1) < p(x|ω2)",
     "P(ω1|x) > P(ω2|x)",
     "p(x) daha büyükse",
     "λ değeri negatifse"],
    2))

answers_mcq.append(mcq(_next(),
    "Maksimum A Posteriori (MAP) kuralı ne yapar?",
    ["Olabilirliği en yüksek sınıfı seçer",
     "Önseli en yüksek sınıfı seçer",
     "Sonsal olasılığı en yüksek sınıfı seçer",
     "Kaybı en yüksek sınıfı seçer",
     "Rastgele seçim yapar"],
    2))

answers_mcq.append(mcq(_next(),
    "Koşullu risk R(αi|x) ne anlama gelir?",
    ["Bir sınıfın önsel olasılığı",
     "Belirli bir x gözlemi için αi eylemini almanın beklenen maliyeti",
     "Sınıflandırıcının doğruluk oranı",
     "Kanıt teriminin değeri",
     "Özellik uzayının hacmi"],
    1))

answers_mcq.append(mcq(_next(),
    "Sıfır-bir kayıp (zero-one loss) kullanıldığında Bayes riski neye eşittir?",
    ["Ortalama hata olasılığına",
     "Önsel olasılığa",
     "Olabilirliğe",
     "Kovaryansa",
     "Entropiye"],
    0))

answers_mcq.append(mcq(_next(),
    "Olabilirlik oranı (likelihood ratio) kuralında eşik θ=1 ne zaman ortaya çıkar?",
    ["Kayıplar asimetrikse",
     "Önseller eşit ve kayıplar simetrikse",
     "Veri çok büyükse",
     "Sınıf sayısı 3’ten fazlaysa",
     "Gauss olmayan dağılımlarda"],
    1))

answers_mcq.append(mcq(_next(),
    "Minimax kriterinin temel motivasyonu nedir?",
    ["Riski sabit tutmak",
     "Önsel olasılıklar bilinmiyor ya da değişkenken en kötü durumdaki riski minimize etmek",
     "Kayıpları 0 yapmak",
     "Özellik sayısını azaltmak",
     "Boyutluluk lanetini çözmek"],
    1))

answers_mcq.append(mcq(_next(),
    "Neyman-Pearson kriteri hangi tür problemler için uygundur?",
    ["Tüm kayıpların eşit olduğu durumlar",
     "Belirli bir sınıfın hata oranını önceden belirlenmiş bir üst sınırla kısıtlamak gerektiğinde",
     "Sadece simetrik Gauss için",
     "Önseller bilindiğinde",
     "Hiçbir kısıt olmadığında"],
    1))

answers_mcq.append(mcq(_next(),
    "Asimetrik kayıpla (λ12 > λ21) ilgili olarak karar sınırı ne yönde kayar?",
    ["Hiçbir yöne kaymaz",
     "ω1 karar bölgesi küçülecek şekilde eşik büyür",
     "ω1 karar bölgesi büyüyecek şekilde eşik küçülür",
     "Her iki bölge de eşit oranda büyür",
     "Kayıp miktarına bağlı değildir"],
    1))

answers_mcq.append(mcq(_next(),
    "Ayırt edici (discriminant) fonksiyonlar için karar kuralı nasıldır?",
    ["gi(x) < gj(x) ise ωi seç",
     "gi(x) = gj(x) ise ωi seç",
     "gi(x) > gj(x) ∀j ≠ i ise ωi seç; yani ω* = argmax gi(x)",
     "gi(x) sıfırsa karar verme",
     "gi(x) negatifse ωj seç"],
    2))

answers_mcq.append(mcq(_next(),
    "Karar yüzeyi (decision surface) hangi koşulda oluşur?",
    ["gi(x) = 0 olduğunda",
     "gi(x) > gj(x) olduğunda",
     "gi(x) = gj(x) olduğunda",
     "Kayıp matrisi tanımsız olduğunda",
     "Özellik sayısı 1’den büyükse"],
    2))

answers_mcq.append(mcq(_next(),
    "Dikotomizer (dichotomizer) tanımı aşağıdakilerden hangisidir?",
    ["Üç ve daha fazla sınıfı ayıran sınıflandırıcı",
     "Yalnızca iki sınıftan birine atama yapan sınıflandırıcı; tek fonksiyon g(x)=g1(x)-g2(x) yeterlidir",
     "Sürekli çıktı veren regresyon",
     "Kümeleme algoritması",
     "Parametrik olmayan özel bir yoğunluk tahmini"],
    1))

answers_mcq.append(mcq(_next(),
    "Karar bölgeleri (decision regions) ile ilgili aşağıdakilerden hangisi doğrudur?",
    ["Her zaman tek parça (simply connected) olmak zorundadır",
     "Her zaman eşit alana sahiptir",
     "Bazen birden fazla ayrık parçadan oluşabilir (not simply connected)",
     "Yalnızca iki boyutta tanımlıdır",
     "Dağılımın cinsine bağlı değildir"],
    2))

answers_mcq.append(mcq(_next(),
    "Sınıf-koşullu yoğunluk fonksiyonu p(x|ωj) neyi ifade eder?",
    ["x ölçüldükten sonra sınıf olasılığını",
     "ωj sınıfındayken x özelliğinin yoğunluğunu (olabilirlik)",
     "Veriyi sıkıştırma oranını",
     "Kayıp matrisinin determinantını",
     "Özellik uzayının hacmini"],
    1))

answers_mcq.append(mcq(_next(),
    "Bayes karar kuralı <b>optimal</b>dir çünkü:",
    ["Her zaman sıfır hata verir",
     "Ortalama hata olasılığını minimize eden kural odur; dağılımlar bilindiğinde daha iyisi yapılamaz",
     "Eğitim süresi en kısadır",
     "Her zaman doğrusal sınır üretir",
     "Belleği az kullanır"],
    1))

answers_mcq.append(mcq(_next(),
    "Aşağıdakilerden hangisi Bayes / Minimax / Neyman-Pearson eşleştirmesinde <b>doğru</b>dur?",
    ["Bayes: kısıt altında risk | Minimax: önseller bilinmiyor | Neyman-Pearson: tüm risk",
     "Bayes: toplam riski minimize et | Minimax: en kötü senaryodaki riski minimize et | Neyman-Pearson: belirli bir kısıt altında riski minimize et",
     "Bayes: en kötü senaryo | Minimax: kısıt altında risk | Neyman-Pearson: toplam risk",
     "Hepsi aynı amacı güder",
     "Minimax maliyetleri görmezden gelir"],
    1))

answers_mcq.append(mcq(_next(),
    "Spam filtresinde λ(α2|spam) » λ(α1|normal) varsayımı ne anlama gelir?",
    ["Normal postayı spam sanmak daha pahalıdır",
     "Spam’i gözden kaçırmak normal postayı spam sanmaktan çok daha pahalıdır",
     "İki hata türünün maliyeti aynıdır",
     "Kayıp matrisinin tüm elemanları negatifdir",
     "Kayıp hiç dikkate alınmaz"],
    1))

answers_mcq.append(mcq(_next(),
    "Çok kategorili durumda genel sınıflandırıcı yapısı ne şekilde çalışır?",
    ["Tüm sınıflara eşit olasılık atar",
     "Girdiden c adet discriminant g1..gc hesaplar, en büyük değere sahip sınıfı seçer",
     "Yalnızca önseli en büyük sınıfı seçer",
     "Özellikleri sıralayıp ilk iki özelliği kullanır",
     "Kayıp matrisi tanımsızsa karar vermez"],
    1))

h2("B. Boşluk Doldurmalı Sorular")

answers_fib.append(fib(_fnext(),
    "Bayes formülüne göre: sonsal = (olabilirlik × __________) / __________.",
    "önsel (prior); kanıt (evidence)"))

answers_fib.append(fib(_fnext(),
    "Bayes karar kuralı, ortalama hata olasılığını __________ eden __________ karar kuralıdır.",
    "minimize; optimal"))

answers_fib.append(fib(_fnext(),
    "Sıfır-bir kayıp kullanıldığında koşullu risk R(αi|x) = 1 − __________ olur.",
    "P(ωi|x)"))

answers_fib.append(fib(_fnext(),
    "Önseller eşit ve kayıplar simetrik olduğunda, iki sınıflı karar yalnızca __________ karşılaştırmasına indirgenir.",
    "olabilirlik (p(x|ω1) ile p(x|ω2))"))

answers_fib.append(fib(_fnext(),
    "__________ kriteri, önsel olasılıklar bilinmediğinde en kötü durumdaki riski minimize etmek üzere tasarlanmıştır.",
    "Minimax"))

answers_fib.append(fib(_fnext(),
    "__________ kriteri, belirli bir sınıf için hata oranını bir üst sınıra kısıtlarken diğer sınıfın hata oranını minimize eder.",
    "Neyman-Pearson"))

answers_fib.append(fib(_fnext(),
    "Ayırt edici fonksiyonlarla karar kuralı: ω* = __________ gi(x).",
    "arg max i"))

answers_fib.append(fib(_fnext(),
    "gi(x) = gj(x) koşulunu sağlayan noktaların oluşturduğu geometrik yapıya __________ denir.",
    "karar yüzeyi (decision surface)"))

answers_fib.append(fib(_fnext(),
    "İki sınıflı sınıflandırıcıya (dikotomizer) tek bir fonksiyonla g(x) = g1(x) − __________ ile indirgenebilir.",
    "g2(x)"))

answers_fib.append(fib(_fnext(),
    "Olabilirlik oranı testi p(x|ω1)/p(x|ω2), __________ değeriyle karşılaştırılarak karar verilir; bu değer hem __________ hem de kayıplara bağlıdır.",
    "eşik (θ); önsel olasılıklara"))

# =====================================================================
# BÖLÜM 3 — PARAMETRİK KESTİRİM (MLE / BAYES / EM)
# =====================================================================
story.append(PageBreak())
h1("BÖLÜM 3 — Parametrik Kestirim: MLE, Bayes, EM")
h2("A. Çoktan Seçmeli Sorular")

answers_mcq.append(mcq(_next(),
    "Parametrik kestirimde temel varsayım nedir?",
    ["Dağılımın formu hakkında hiçbir şey bilinmez",
     "Dağılımın formu bilinir, yalnızca parametreleri veriden tahmin edilir",
     "Veri etiketsizdir",
     "Yoğunluk fonksiyonu doğrudan verilir",
     "Parametreler sabittir, tahmin edilmez"],
    1))

answers_mcq.append(mcq(_next(),
    "Maximum Likelihood Estimation (MLE) hangi prensibe dayanır?",
    ["Eldeki veriyi en olası kılan parametreyi seçmek (olabilirliği maksimize etmek)",
     "Önsel bilgiyi maksimize etmek",
     "Kanıtı (evidence) maksimize etmek",
     "Veriyi dönüştürüp sıkıştırmak",
     "Hataları karesini almamak"],
    0))

answers_mcq.append(mcq(_next(),
    "Log-olabilirlik kullanmanın temel nedenlerinden hangisi <b>yanlıştır</b>?",
    ["Çarpımı toplama çevirip underflow sorununu önlemek",
     "Türev almayı kolaylaştırmak",
     "Numerik kararlılığı artırmak",
     "Maksimum noktasının yerini değiştirmek",
     "Hesaplamayı hızlandırmak"],
    3,
    "Logaritma monoton arttığından maksimumun yeri değişmez."))

answers_mcq.append(mcq(_next(),
    "Gaussian dağılım için MLE ortalama tahmini aşağıdakilerden hangisidir?",
    ["Örneklerin medyanı",
     "Örneklerin aritmetik ortalaması",
     "Örneklerin modu",
     "Örneklerin varyansının karekökü",
     "Örneklerin minimumu"],
    1))

answers_mcq.append(mcq(_next(),
    "Gaussian için MLE varyans tahmini nedir?",
    ["Sapmaların aritmetik ortalaması",
     "Ortalamadan karesel sapmaların aritmetik ortalaması",
     "Sapmaların karekökü",
     "Sapmaların logaritmasının toplamı",
     "Ortalamanın karesi"],
    1))

answers_mcq.append(mcq(_next(),
    "Çok değişkenli Gaussian için kovaryans matrisi <b>köşegen dışı</b> elemanları ne anlatır?",
    ["Her özelliğin ayrı varyansı",
     "İki özelliğin birlikte hareket ettiğini gösteren kovaryans",
     "Her zaman sıfır olmak zorundadır",
     "Özelliklerin ortalaması",
     "Özelliklerin medyanı"],
    1))

answers_mcq.append(mcq(_next(),
    "Bayesian kestirimde parametre nasıl ele alınır?",
    ["Sabit, tek bir değer olarak",
     "Belirli bir dağılımı (önsel) olan rastgele değişken olarak; veri geldikçe sonsal dağılımıyla güncellenir",
     "Her zaman sıfır alınır",
     "Eğitim verisinin medyanı olarak",
     "Asla güncellenmez"],
    1))

answers_mcq.append(mcq(_next(),
    "MLE ile Bayesian kestirim arasındaki farkı en iyi açıklayan ifade hangisidir?",
    ["MLE’de veri yok sayılır",
     "Bayesian’da veri yok sayılır",
     "MLE yalnızca veriye bakar; Bayesian ise önsel bilgi ile veriyi birleştirir. Az veride Bayesian daha güvenilirdir",
     "İkisi tamamen aynı sonucu verir",
     "MLE hiçbir varsayım yapmaz"],
    2))

answers_mcq.append(mcq(_next(),
    "Bayesian güncellemede σn² < σ² olması ne anlama gelir?",
    ["Veri parametreden daha belirsizdir",
     "Önsel yanlıştır",
     "Veri toplandıkça parametre hakkındaki belirsizlik azalır",
     "Gürültü sıfırlanmıştır",
     "Önsel ortalaması değişmiştir"],
    2))

answers_mcq.append(mcq(_next(),
    "Dar (bilgi açısından güçlü) önsel ile geniş (belirsiz) önsel arasındaki davranış farkı için aşağıdakilerden hangisi doğrudur?",
    ["Dar önsel veriye daha çok söz verir",
     "Geniş önsel veriye daha çok söz verir; dar önsel ön bilgiyi baskın kılar",
     "İkisi aynı davranır",
     "Geniş önsel her zaman daha iyidir",
     "Dar önsel her zaman daha iyidir"],
    1))

answers_mcq.append(mcq(_next(),
    "Veri sayısı n → ∞ iken Bayesian kestirim ile MLE arasında ne olur?",
    ["Bayesian kestirim tamamen sıfıra gider",
     "İki yöntem aynı sonuca yakınsar",
     "Bayesian daima daha iyidir",
     "MLE tamamen belirsiz hâle gelir",
     "Önsel varyans büyür"],
    1))

answers_mcq.append(mcq(_next(),
    "Boyutluluk laneti (curse of dimensionality) nedir?",
    ["Boyut arttıkça hesaplama süresinin azalması",
     "Özellik sayısı arttıkça iyi bir tahmin için gereken veri miktarının üstel olarak artması",
     "Özellik sayısının asla artmaması",
     "Boyutun sınıflandırıcıyı otomatik güçlendirmesi",
     "Yalnızca yoğun verilerde görülmesi"],
    1))

answers_mcq.append(mcq(_next(),
    "Aşırı öğrenme (overfitting) için hangisi doğrudur?",
    ["Eğitim hatası yüksek, test hatası düşüktür",
     "Eğitim hatası düşük, test hatası yüksektir; eğitim ve test hataları arasındaki makas açılır",
     "Eğitim ve test hataları eşittir",
     "Aşırı öğrenme yalnızca doğrusal modellerde görülür",
     "Daha fazla veri eklemek daima durumu kötüleştirir"],
    1))

answers_mcq.append(mcq(_next(),
    "Expectation-Maximization (EM) algoritması hangi durumda kullanılır?",
    ["Veri tamamen etiketliyse",
     "Verinin bir kısmı (örn. etiketler) gözlemlenemediğinde, log-olabilirliği doğrudan maksimize etmek zor olduğunda",
     "Veri hiç olmadığında",
     "Parametre sayısı sıfırsa",
     "Dağılım düzgün dağılımsa"],
    1))

answers_mcq.append(mcq(_next(),
    "EM algoritmasında E-adımı ve M-adımı sırasıyla ne yapar?",
    ["E: veriyi sil, M: veriyi yeniden oluştur",
     "E: mevcut parametrelerle her örneğin hangi gruba ait olduğunu tahmin et; M: bu atamalarla parametreleri güncelle",
     "E: yalnızca ortalamayı hesapla; M: yalnızca varyansı hesapla",
     "E: gözlemi unut; M: parametreyi unut",
     "E: veri topla; M: veri sil"],
    1))

answers_mcq.append(mcq(_next(),
    "EM algoritmasının yakınsama özelliği aşağıdakilerden hangisidir?",
    ["Her iterasyonda parametreler ya iyileşir ya da aynı kalır; geriye gitmez",
     "Her iterasyonda kötüleşir",
     "Sadece rastgele değişir",
     "Hiçbir zaman yakınsamaz",
     "Tek bir adımda biter"],
    0))

answers_mcq.append(mcq(_next(),
    "Gaussian Karışım Modeli (GMM) ne zaman kullanılır?",
    ["Veri tek bir Gauss ile mükemmel açıklanıyorsa",
     "Veri çok modlu / birden fazla gruptan geliyorsa; her grup bir Gauss ile temsil edilir",
     "Yalnızca denetimli sınıflandırmada",
     "Yoğunluk parametrik olmadığında",
     "Veri tamamen etiketliyse asla gerekmez"],
    1))

answers_mcq.append(mcq(_next(),
    "GMM’de πk karışım ağırlığı ne ifade eder?",
    ["k. bileşenin ortalaması",
     "k. bileşenin varyansı",
     "Bir örneğin k. bileşene ait olma olasılığı (karışım oranı)",
     "k. bileşenin kovaryans determinantı",
     "k. bileşenin entropisi"],
    2))

answers_mcq.append(mcq(_next(),
    "Boyutluluk lanetine karşı pratikte ne önerilir?",
    ["Mümkün olduğunca çok özellik eklemek",
     "Az ama anlamlı özellikler seçmek; gereksiz özelliklerden kaçınmak",
     "Etiketleri rastgele atamak",
     "Test verisini eğitime karıştırmak",
     "Modeli karmaşıklaştırmak"],
    1))

answers_mcq.append(mcq(_next(),
    "Bayesian güncelleme formülü hangisidir?",
    ["p(θ|D) ∝ p(θ) / p(D|θ)",
     "p(θ|D) = p(D|θ) − p(θ)",
     "p(θ|D) ∝ p(D|θ) · p(θ)  (sonsal ∝ olabilirlik × önsel)",
     "p(θ|D) = 1 − p(θ)",
     "p(θ|D) = p(D)·p(θ)"],
    2))

h2("B. Boşluk Doldurmalı Sorular")

answers_fib.append(fib(_fnext(),
    "MLE, __________ (likelihood) fonksiyonunu maksimize eden parametre değerini tahmin olarak seçer.",
    "olabilirlik"))

answers_fib.append(fib(_fnext(),
    "Çarpımları toplamlara çevirip türev almayı kolaylaştırmak ve underflow’u önlemek için olabilirlik yerine __________ kullanılır.",
    "log-olabilirlik (log-likelihood)"))

answers_fib.append(fib(_fnext(),
    "Gaussian dağılım için MLE ortalaması örneklerin __________’ıdır; varyansı ise ortalamadan __________ sapmaların ortalamasıdır.",
    "aritmetik ortalaması; karesel"))

answers_fib.append(fib(_fnext(),
    "Çok değişkenli Gauss’ta özelliklerin birlikte nasıl hareket ettiğini __________ matrisi yakalar.",
    "kovaryans (Σ)"))

answers_fib.append(fib(_fnext(),
    "Bayes kestiriminde, veriyi görmeden önceki bilgi __________ dağılımı ile ifade edilir; veri geldikten sonra bu bilgi __________ dağılımı ile güncellenir.",
    "önsel (prior); sonsal (posterior)"))

answers_fib.append(fib(_fnext(),
    "Veri sayısı sonsuza giderken Bayesian kestirim __________ kestirimi ile aynı sonuca yakınsar.",
    "MLE"))

answers_fib.append(fib(_fnext(),
    "Özellik sayısı arttıkça iyi bir tahmin için gereken veri miktarının üstel olarak artmasına __________ denir.",
    "boyutluluk laneti (curse of dimensionality)"))

answers_fib.append(fib(_fnext(),
    "EM algoritması __________ adımında gizli değişkenlerin beklenti değerini hesaplar, __________ adımında ise parametreleri günceller.",
    "E (Expectation); M (Maximization)"))

answers_fib.append(fib(_fnext(),
    "Veri birden fazla alt-dağılımdan geliyorsa bunu modellemek için kullanılan karışım modeline __________ denir ve parametreleri genellikle __________ algoritmasıyla öğrenilir.",
    "Gaussian Karışım Modeli (GMM); EM"))

answers_fib.append(fib(_fnext(),
    "Model eğitim verisini ezberleyip yeni verilerde kötü sonuç veriyorsa buna __________ denir; en etkili çözüm daha fazla __________ toplamaktır.",
    "aşırı öğrenme (overfitting); veri"))

# =====================================================================
# BÖLÜM 4 — PARZEN PENCERELERİ (PARAMETRİK OLMAYAN YÖNTEMLER)
# =====================================================================
story.append(PageBreak())
h1("BÖLÜM 4 — Parzen Pencereleri ve Parametrik Olmayan Yoğunluk Kestirimi")
h2("A. Çoktan Seçmeli Sorular")

answers_mcq.append(mcq(_next(),
    "Parametrik olmayan (non-parametric) yöntemlerin temel fikri nedir?",
    ["Dağılım için bir form varsaymak ve yalnızca parametrelerini tahmin etmek",
     "Yoğunluk fonksiyonunun formu hakkında önceden hiçbir varsayım yapmadan doğrudan veriden kestirmek",
     "Eğitim verisini tamamen silmek",
     "Her zaman Gauss dağılımı varsaymak",
     "Yalnızca etiketli veri kullanmak"],
    1))

answers_mcq.append(mcq(_next(),
    "Parametrik yöntemlerin “tek modlu dağılım varsayımı” neden sorunludur?",
    ["Çoklu modlu dağılımlar nadir görülür",
     "Gerçek dünyadaki birçok problem çok modlu olduğundan tek bir Gauss bu yapıları temsil edemez ve model yanlılığı oluşur",
     "Tek modlu dağılım hesaplanması zordur",
     "Tek modlu dağılım MLE ile çözülemez",
     "Parametrik yöntemler etiket gerektirmediği için"],
    1))

answers_mcq.append(mcq(_next(),
    "Parametrik olmayan yoğunluk kestirim formülü p(x) ≈ k/(nV) için hangi ifade <b>yanlıştır</b>?",
    ["k: R bölgesi içindeki örnek sayısı",
     "n: toplam örnek sayısı",
     "V: bölge hacmi",
     "Yoğunluk, yalnızca ham sayım k ile belirlenir, hacimle ilişkisi yoktur",
     "Kestirim yerel veri yoğunluğunu bölge büyüklüğüne bölerek verir"],
    3))

answers_mcq.append(mcq(_next(),
    "Histogram yaklaşımında “kutu genişliği (bin width)” neden kritik bir hiperparametredir?",
    ["Kutu genişliği dağılımın ortalamasını belirler",
     "Çok küçük seçilirse kutular boş kalır, çok büyük seçilirse detaylar kaybolur; yöntem başarısını doğrudan etkiler",
     "Kutu genişliği yoğunluk kestirimini hiç etkilemez",
     "Kutu genişliği her zaman veri sayısına eşit seçilmelidir",
     "Kutu genişliği negatif seçilmelidir"],
    1))

answers_mcq.append(mcq(_next(),
    "Parzen pencereleri ile k-NN arasındaki temel fark nedir?",
    ["İkisi tamamen aynıdır",
     "Parzen’de V sabit, k değişken; k-NN’de k sabit, V değişkendir",
     "Parzen etiketli veri gerektirir, k-NN gerektirmez",
     "Parzen pencerelerinde V veriye göre değişir",
     "k-NN’de yoğunluk tanımsızdır"],
    1))

answers_mcq.append(mcq(_next(),
    "Parzen penceresinin temel varsayımlarından biri hiperküp penceresidir. d-boyutlu uzayda kenar uzunluğu h olan hiperküpün hacmi nedir?",
    ["h", "h + d", "h^d", "d·h", "2h"],
    2))

answers_mcq.append(mcq(_next(),
    "Pencere fonksiyonu φ(u) (kutu kernel) hangi değerleri alır?",
    ["Her zaman Gauss eğrisi şeklinde değerler",
     "|uj| ≤ 1/2 koşulunu sağlayan bileşenler için 1, aksi hâlde 0",
     "Her zaman 1",
     "Negatif değerler",
     "Yalnızca tam sayılar"],
    1))

answers_mcq.append(mcq(_next(),
    "Parzen yoğunluğunun analitik formu p_φ(x) = (1/n) Σ (1/h^d) φ((x-xi)/h) ifadesinde 1/h^d çarpanının amacı nedir?",
    ["Toplam olasılığı 0 yapmak",
     "Hacme göre ölçekleme (normalizasyon)",
     "Veri sayısını artırmak",
     "Yalnızca hesaplamayı yavaşlatmak",
     "Etiketleri silmek"],
    1))

answers_mcq.append(mcq(_next(),
    "Hiperküp (box) kernel’in temel dezavantajı nedir?",
    ["Çok yavaştır",
     "Yalnızca yüksek boyutta çalışır",
     "Pencere içindeki tüm noktalara eşit ağırlık verir; mesafe bilgisini göz ardı eder ve basamaklı (süreksiz) eğri üretir",
     "Yalnızca Gauss dağılımıyla çalışır",
     "Etiket gerektirir"],
    2))

answers_mcq.append(mcq(_next(),
    "Kernel Density Estimation (KDE) için hangisi <b>doğrudur</b>?",
    ["Pencere fonksiyonunun integrali sıfıra eşit olmalıdır",
     "Pencere fonksiyonu negatif olmayan, integrali 1 olan herhangi bir fonksiyon olabilir",
     "Yalnızca kutu kernel kullanılabilir",
     "Bant genişliği h’nin etkisi yoktur",
     "KDE bir parametrik yöntemdir"],
    1))

answers_mcq.append(mcq(_next(),
    "Gaussian kernel, kutu kernel’e göre hangi iki problemi çözer?",
    ["Overfitting ve underfitting",
     "Mesafe duyarsızlığı ve süreksizlik problemleri",
     "Hesaplama karmaşıklığı ve boyutluluk laneti",
     "Etiket eksikliği ve veri sayısı azlığı",
     "Gürültü ve sensör arızası"],
    1))

answers_mcq.append(mcq(_next(),
    "Parzen yönteminde bant genişliği h’nin etkisi için hangisi doğrudur?",
    ["h küçükse çok pürüzsüz, h büyükse çok dalgalı eğri üretir",
     "h küçükse dalgalı (yüksek varyans), h büyükse aşırı düzleşmiş (yüksek yanlılık) kestirim üretir",
     "h’nin kestirim üzerinde hiçbir etkisi yoktur",
     "h yalnızca kutu kernel için geçerlidir",
     "h büyüdükçe kestirim daima iyileşir"],
    1))

answers_mcq.append(mcq(_next(),
    "n → ∞ iken Parzen yönteminin yakınsaması için hangi koşullar gereklidir?",
    ["Vn → ∞ ve nVn → 0",
     "Vn → 0 ve nVn → ∞",
     "Vn = sabit ve n = sabit",
     "Vn → 0 ve n → 0",
     "Vn’nin yok olması gerekmez"],
    1))

answers_mcq.append(mcq(_next(),
    "n sabitken doğruluğu artırmanın tek yolu bölge boyutunu küçültmektir. Bu yaklaşımın sınırı nedir?",
    ["Bölge çok küçük olursa içine hiç veri düşmez ve p(x) ≈ 0 hatası olur",
     "Sınır yoktur, her zaman güvenlidir",
     "Bölge küçükse sınıflandırma hızlanır ama başka bir olumsuzluk yoktur",
     "Veri sayısını artırır",
     "Bölge küçükse ortalama hata sıfırdır"],
    0))

answers_mcq.append(mcq(_next(),
    "Aşağıdakilerden hangisi histogram ile Parzen yöntemi arasındaki <b>en belirgin</b> farktır?",
    ["İkisi de etiket gerektirir",
     "Histogramda kutular sabittir; Parzen’de her x için pencere o noktanın etrafına yeniden kurulur (sliding window)",
     "Parzen yönteminde kutular çakışmaz",
     "Histogram yalnızca parametrik modellerde çalışır",
     "Parzen yalnızca tek boyutta kullanılır"],
    1))

h2("B. Boşluk Doldurmalı Sorular")

answers_fib.append(fib(_fnext(),
    "Parametrik olmayan yöntemler, dağılım formu hakkında hiçbir __________ (ön varsayım) gerektirmeden yalnızca eğitim verilerinden yoğunluğu kestirir.",
    "önsel (prior) / varsayım"))

answers_fib.append(fib(_fnext(),
    "Yoğunluk kestiriminin ortak formülü p(x) ≈ k / (n · __________) şeklindedir.",
    "V (bölge hacmi)"))

answers_fib.append(fib(_fnext(),
    "Parzen pencerelerinde __________ sabit tutulurken içindeki veri sayısı değişir; k-NN’de ise __________ sabit tutulurken bölge hacmi değişir.",
    "V (bölge hacmi); k (komşu sayısı)"))

answers_fib.append(fib(_fnext(),
    "Pencere fonksiyonunun daha genel biçimi olarak, integrali 1 ve negatif olmayan her fonksiyonun kullanılabildiği yönteme __________ (KDE) denir.",
    "Çekirdek Yoğunluk Kestirimi (Kernel Density Estimation)"))

answers_fib.append(fib(_fnext(),
    "Kutu kernel basamaklı ve süreksiz eğri üretirken, __________ kernel pürüzsüz (smooth) ve türevlenebilir eğri verir.",
    "Gaussian"))

answers_fib.append(fib(_fnext(),
    "Parzen yönteminde bant genişliği h çok küçükse yüksek __________, çok büyükse yüksek __________ elde edilir.",
    "varyans (dalgalı, overfit); yanlılık (aşırı düzleşme, underfit)"))

answers_fib.append(fib(_fnext(),
    "d-boyutlu hiperküpün kenar uzunluğu h ise hacmi V = __________ olur.",
    "h^d"))

answers_fib.append(fib(_fnext(),
    "Histogramda kutular birbirine __________ değildir ve tüm uzayı __________ eder.",
    "çakışmaz; bölümler (partition)"))

answers_fib.append(fib(_fnext(),
    "Parzen yönteminin Gaussian kernel ile pürüzsüz hale gelmesinin asıl nedeni, her veri noktasının yakınlık derecesine göre farklı __________ ile hesaba katılmasıdır.",
    "ağırlıklar"))

answers_fib.append(fib(_fnext(),
    "Parzen yakınsaması için gerekli koşullar: Vn → __________ ve n·Vn → __________.",
    "0; ∞"))

# =====================================================================
# BÖLÜM 5 — k-EN YAKIN KOMŞU (k-NN)
# =====================================================================
story.append(PageBreak())
h1("BÖLÜM 5 — k-En Yakın Komşu (k-NN) ve Voronoi")
h2("A. Çoktan Seçmeli Sorular")

answers_mcq.append(mcq(_next(),
    "k-NN yoğunluk kestiriminde hangi büyüklük sabit tutulur?",
    ["Bölge hacmi V",
     "Komşu sayısı k",
     "Veri sayısı n",
     "Bant genişliği h",
     "Özellik sayısı d"],
    1))

answers_mcq.append(mcq(_next(),
    "k-NN’in Parzen’e göre temel avantajı nedir?",
    ["Her zaman daha hızlıdır",
     "Pencere genişliği h seçme zorunluluğu yoktur; model yoğunluğa otomatik olarak uyum sağlar (adaptif)",
     "Etiket gerektirmez",
     "Her zaman daha düşük bellek kullanır",
     "Tek boyutta çalışır"],
    1))

answers_mcq.append(mcq(_next(),
    "k-NN ile doğrudan yoğunluk kestirimi pratikte neden iyi çalışmaz?",
    ["Sonuç her zaman geçerli bir yoğunluk fonksiyonu olmaz, süreksizlikler içerir ve kuyrukları gereğinden ağırdır",
     "k-NN yalnızca sınıflandırma için tanımlıdır",
     "Veri eksikliğinde de mükemmel çalışır",
     "Sıfır hata verir",
     "Gauss dağılımı varsayar"],
    0))

answers_mcq.append(mcq(_next(),
    "k-NN sınıflandırıcısının karar kuralı nedir?",
    ["En yakın komşunun sınıfı her zaman seçilir",
     "En uzak komşunun sınıfı seçilir",
     "En yakın k komşuya bakılır ve çoğunluk oylaması (majority voting) ile sınıf atanır",
     "Rastgele bir komşu seçilir",
     "Tüm veri noktalarının sınıf ortalaması alınır"],
    2))

answers_mcq.append(mcq(_next(),
    "1-NN için Voronoi diyagramı ne gösterir?",
    ["Her veri noktasının kendi etki alanını; komşu hücre sınırları iki noktaya eşit uzaklıktadır ve bu sınırlar aynı zamanda karar sınırlarıdır",
     "Eğitim verisinin histogramını",
     "Bayes karar yüzeyini",
     "Parzen penceresinin hacmini",
     "Sadece 3 boyutta tanımlıdır"],
    0))

answers_mcq.append(mcq(_next(),
    "k değerinin seçimi için aşağıdakilerden hangisi doğrudur?",
    ["Küçük k daima daha iyidir",
     "Büyük k daima daha iyidir",
     "k çok küçükse karar sınırları gürültülü olur; k çok büyükse uzak, alakasız noktalar da dahil olup sınır bölgelerinde hata yapar. Denge kurmak gerekir",
     "k seçiminin model performansıyla ilgisi yoktur",
     "k, veri sayısına eşit seçilmelidir"],
    2))

answers_mcq.append(mcq(_next(),
    "k-NN’in hesaplama karmaşıklığı genellikle aşağıdakilerden hangisidir?",
    ["O(1)",
     "O(log n)",
     "O(knd)",
     "O(n²)",
     "O(d!)"],
    2))

answers_mcq.append(mcq(_next(),
    "Arama ağaçları ve prototip tabanlı yapılar k-NN’de neden kullanılır?",
    ["Karar sınırını tamamen ortadan kaldırmak için",
     "Tüm veri üzerinde tek tek arama yapmak yerine benzerliklere göre organize edilmiş bir yapıda daha hızlı arama yapmak için",
     "Etiketleri oluşturmak için",
     "Özellik çıkarımı yapmak için",
     "Veriyi rastgele etiketlemek için"],
    1))

answers_mcq.append(mcq(_next(),
    "k-NN’in temel çelişkisi (paradoksu) nedir?",
    ["Az veri daha iyi doğruluk verir",
     "İyi çalışması için çok veri gerekir; ancak veri arttıkça hesaplama maliyeti de hızla artar",
     "Yüksek boyut daima daha iyi sonuç verir",
     "Normalize edilmiş veri her zaman kötüdür",
     "Büyük k daima daha iyidir"],
    1))

answers_mcq.append(mcq(_next(),
    "Öklid mesafesinin k-NN’de ortaya çıkan temel sorunu nedir?",
    ["Negatif değerler üretmesi",
     "Tüm özelliklere eşit ağırlık vermesi; oysa bazı özellikler sınıfları ayırmada çok daha etkili olabilir",
     "Yalnızca tek boyutta tanımlı olması",
     "Her zaman 1 değerini vermesi",
     "Üçgen eşitsizliğini sağlamaması"],
    1))

answers_mcq.append(mcq(_next(),
    "Özellik ağırlıklandırma (feature weighting) ne amaçla kullanılır?",
    ["Önemsiz özellikleri daha belirgin hale getirmek için",
     "Önemli özellikleri öne çıkarmak, az önemli olanların etkisini azaltmak için",
     "Sadece Gauss dağılımı oluşturmak için",
     "Verinin boyutunu artırmak için",
     "Etiketleri silmek için"],
    1))

answers_mcq.append(mcq(_next(),
    "Farklı ölçeklerdeki özellikler için z-score normalizasyonu (x' = (x−μ)/σ) neden uygulanır?",
    ["Tüm özelliklerin ortalamasını 1, varyansını 0 yapmak için",
     "Her özelliği aynı ölçeğe getirerek mesafenin büyük ölçekli özellik tarafından dominanas edilmesini engellemek için",
     "Etiketleri dengelemek için",
     "Özellik sayısını azaltmak için",
     "Verinin modunu kaldırmak için"],
    1))

answers_mcq.append(mcq(_next(),
    "Özellik ölçekleri çok farklıysa (örn. biri 1-2, diğeri 100-200) normalize edilmemiş k-NN’de ne olur?",
    ["Her özellik eşit oranda katkı yapar",
     "Mesafeyi neredeyse tamamen büyük ölçekli özellik belirler, küçük ölçekli özellik kaybolur",
     "Küçük ölçekli özellik her zaman baskın olur",
     "Hiçbir şey değişmez",
     "Sınıflandırma daima doğru olur"],
    1))

answers_mcq.append(mcq(_next(),
    "1-NN kararı için Voronoi hücresi hangi noktaların kümesidir?",
    ["Bir referans noktadan eşit uzaklıkta olan noktalar",
     "Belirli bir eğitim noktasına (xi) diğer tüm eğitim noktalarından daha yakın olan tüm noktalar",
     "Uzayın orijinine en yakın noktalar",
     "Merkezden belirli bir yarıçapta olan noktalar",
     "Aynı sınıfa sahip tüm noktalar"],
    1))

answers_mcq.append(mcq(_next(),
    "Teorik olarak veri sayısı sonsuzsa k büyüdükçe k-NN hata oranı hangi değere yakınsar?",
    ["Bayes hatasına", "Sıfıra", "1’e", "Önsel olasılığa", "Bant genişliğine"],
    0))

h2("B. Boşluk Doldurmalı Sorular")

answers_fib.append(fib(_fnext(),
    "k-NN yoğunluk kestiriminde komşu sayısı __________ sabit tutulur; bölge hacmi __________ ise veriden belirlenir.",
    "k; V"))

answers_fib.append(fib(_fnext(),
    "k = 1 durumunda uzayın her veri noktasına göre bölümlenmesine __________ diyagramı denir.",
    "Voronoi"))

answers_fib.append(fib(_fnext(),
    "k-NN sınıflandırıcısı karar verirken __________ oylaması kullanır.",
    "çoğunluk (majority voting)"))

answers_fib.append(fib(_fnext(),
    "k çok küçük seçilirse karar sınırı __________ olur; k çok büyük seçilirse karar sınırı __________ hale gelir.",
    "gürültülü (overfit); fazla düzleşmiş (underfit)"))

answers_fib.append(fib(_fnext(),
    "k-NN’in zaman karmaşıklığı yaklaşık __________ seviyesindedir.",
    "O(knd)"))

answers_fib.append(fib(_fnext(),
    "Tüm özelliklere eşit ağırlık vermek yerine, her özellik için bir w_k __________ ekleyerek mesafe tanımını iyileştirebiliriz.",
    "ağırlığı"))

answers_fib.append(fib(_fnext(),
    "z-score normalizasyonu sonrası her özelliğin ortalaması __________, varyansı __________ olur.",
    "0; 1"))

answers_fib.append(fib(_fnext(),
    "k-NN yaklaşımını hızlandırmak için veriyi hiyerarşik olarak organize eden __________ yapıları kullanılabilir; ancak bu durum en yakın komşunun her zaman bulunabilmesini __________.",
    "arama ağacı (search tree) / prototip; garanti etmez"))

answers_fib.append(fib(_fnext(),
    "Öklid mesafesi her özelliği __________ önemde kabul eder; bu varsayım gerçek problemlerde çoğunlukla __________.",
    "eşit; doğru değildir"))

answers_fib.append(fib(_fnext(),
    "k-NN ile doğrudan yoğunluk kestirimi, sonucu geçerli bir __________ fonksiyonu yapmayabilir ve eğri çok sayıda __________ içerir.",
    "yoğunluk; süreksizlik"))

# =====================================================================
# BÖLÜM 6 — BAYESIAN BELIEF NETWORKS
# =====================================================================
story.append(PageBreak())
h1("BÖLÜM 6 — Bayesian Belief Networks (BBN)")
h2("A. Çoktan Seçmeli Sorular")

answers_mcq.append(mcq(_next(),
    "Bayesian Belief Network (BBN) en genel tanımıyla nedir?",
    ["Rastgele değişkenler arasındaki koşullu bağımlılıkları yönlü çevrimsiz çizge (DAG) ile ifade eden olasılıksal grafik modeldir",
     "Yalnızca sürekli değişkenler için tanımlı bir regresyon modelidir",
     "Etiketsiz veride kümeleme algoritmasıdır",
     "Evrişimli sinir ağıdır",
     "Kural tabanlı bir uzman sistemdir"],
    0))

answers_mcq.append(mcq(_next(),
    "BBN’de düğümler ve kenarlar ne ifade eder?",
    ["Düğümler olasılık değerleri, kenarlar sabitlerdir",
     "Düğümler rastgele değişkenleri, yönlü kenarlar bağımlılık ilişkilerini (ebeveyn→çocuk) ifade eder",
     "Düğümler veri noktaları, kenarlar etiketlerdir",
     "Düğümler eylemler, kenarlar maliyetlerdir",
     "Düğümler etiketler, kenarlar zaman aralıklarıdır"],
    1))

answers_mcq.append(mcq(_next(),
    "DAG’ın bir BBN olarak kullanılması için aşağıdaki özelliklerden hangisi <b>zorunludur</b>?",
    ["Çevrim (cycle) içermemesi",
     "Tüm kenarların yönsüz olması",
     "Her düğümün en az iki ebeveyni olması",
     "Tüm değişkenlerin sürekli olması",
     "Tüm düğümlerin bağımsız olması"],
    0))

answers_mcq.append(mcq(_next(),
    "Naive Bayes ile BBN arasındaki temel fark nedir?",
    ["İkisi de tamamen aynıdır",
     "Naive Bayes tüm özellikleri bağımsız varsayar; BBN, değişkenler arasındaki bağımlılıkları DAG yapısıyla modelleyebilir",
     "Naive Bayes veri gerektirmez",
     "BBN yalnızca sürekli değişkenlerle çalışır",
     "Naive Bayes etiket gerektirmez"],
    1))

answers_mcq.append(mcq(_next(),
    "BBN’de bir değişkenin olasılığı nelere bağlıdır?",
    ["Ağdaki tüm değişkenlere",
     "Hiçbir değişkene bağlı değildir",
     "Yalnızca ebeveyn düğümlerine (parents)",
     "Yalnızca çocuk düğümlerine",
     "Yalnızca kardeş düğümlere"],
    2))

answers_mcq.append(mcq(_next(),
    "BBN’de birleşik olasılık dağılımı (joint probability) için genel formül nedir?",
    ["P(X1,...,Xn) = Σ P(Xi)",
     "P(X1,...,Xn) = ∏ P(Xi | Parents(Xi))",
     "P(X1,...,Xn) = ∏ P(Xi) (bağımsız varsayım)",
     "P(X1,...,Xn) = P(X1)·P(Xn)",
     "P(X1,...,Xn) = 1 / n"],
    1))

answers_mcq.append(mcq(_next(),
    "Koşullu Olasılık Tablosu (CPT) ne içerir?",
    ["Bir değişkenin ebeveynlerinin her olası kombinasyonu için o değişkenin koşullu olasılıklarını",
     "Yalnızca marjinal olasılıkları",
     "Veri setinin ortalamasını",
     "Yalnızca önsel olasılıkları",
     "Regresyon katsayılarını"],
    0))

answers_mcq.append(mcq(_next(),
    "BBN’in bağımsızlık varsayımına göre koşullu olasılık hesabı P(X|Y) iki değişken bağımsızsa aşağıdakilerden hangisine indirgenir?",
    ["P(X|Y) = 0",
     "P(X|Y) = P(X,Y)",
     "P(X|Y) = P(X)",
     "P(X|Y) = P(Y)",
     "P(X|Y) = 1"],
    2))

answers_mcq.append(mcq(_next(),
    "Bayesian çıkarım (inference) BBN’de hangi gücü sağlar?",
    ["Yalnızca nedenlerden sonuçlara ileri hesap",
     "Hem ileri (nedenden sonuca) hem de ters (sonuçtan nedene) çıkarım yapabilme",
     "Veri silme",
     "Yalnızca ortalama hesabı",
     "Yalnızca özellik seçimi"],
    1))

answers_mcq.append(mcq(_next(),
    "Hava durumu örneğinde çimin ıslak olduğu gözlemlenince P(R|G) değerinin artması ne gösterir?",
    ["Gözlemin hipoteze hiçbir etkisi olmadığını",
     "Kanıt geldikten sonra inancın Bayes formülüyle güncellendiğini; P(R) değerinin güncellenerek P(R|G)’ye dönüştüğünü",
     "Yağmur olasılığının sıfırlandığını",
     "Grafik yapısının kendiliğinden değiştiğini",
     "Ebeveyn düğümlerin silindiğini"],
    1))

answers_mcq.append(mcq(_next(),
    "BBN’in aşağıdaki avantajlarından hangisi <b>yanlıştır</b>?",
    ["Eksik veri toleransına sahiptir",
     "Değişkenler arası ilişkileri modelleyebilir",
     "Görsel ve sezgisel yapıya sahiptir",
     "Yeni kanıt geldiğinde olasılıklar anında güncellenebilir",
     "Değişken sayısı arttıkça hesaplama karmaşıklığı düşer"],
    4))

answers_mcq.append(mcq(_next(),
    "BBN’in dezavantajlarından <b>olmayan</b> hangisidir?",
    ["Overfitting riski",
     "DAG oluşturmanın karmaşıklığı ve alan uzmanlığı gerektirebilmesi",
     "Değişken sayısı arttıkça üstel büyüyen olasılık tabloları",
     "Sürekli değişkenler için ek düzenleme gerektirmesi",
     "Değişkenler arası ilişkileri modelleyememe"],
    4))

answers_mcq.append(mcq(_next(),
    "Aşağıdakilerden hangisi BBN’in <b>uygulama alanı değildir</b>?",
    ["Tıbbi teşhis", "Spam filtreleme", "Gen düzenleme ağları",
     "Sosyal ağ analizi (liderlik tespiti)", "Lineer cebirde determinant hesaplama"],
    4))

answers_mcq.append(mcq(_next(),
    "BBN’de gözlem geldikten sonra inancı güncellemenin temel aracı hangisidir?",
    ["Bayes formülü: P(H|E) = P(E|H)·P(H)/P(E)",
     "Markov özelliği",
     "Gradyan inişi",
     "Viterbi algoritması",
     "k-ortalamalar"],
    0))

answers_mcq.append(mcq(_next(),
    "Sosyal ağ analizinde (SNA) BBN kullanımı için aşağıdakilerden hangisi uygundur?",
    ["Yalnızca ağın görselleştirilmesi",
     "Düğüm önemi (derece/bağlantı merkeziliği), potansiyel lider tespiti ve grup üyeliği tahmini gibi belirsizlik içeren problemler",
     "Veritabanı sorgulama",
     "Derleme hatası tespiti",
     "İşletim sistemi çizelgelemesi"],
    1))

h2("B. Boşluk Doldurmalı Sorular")

answers_fib.append(fib(_fnext(),
    "BBN, rastgele değişkenler arasındaki koşullu bağımlılıkları __________ adı verilen yönlü çevrimsiz çizge ile temsil eden olasılıksal grafik modeldir.",
    "DAG (Directed Acyclic Graph)"))

answers_fib.append(fib(_fnext(),
    "Bir BBN’de düğümler __________ değişkenleri, kenarlar ise bu değişkenler arasındaki __________ ilişkilerini temsil eder.",
    "rastgele; bağımlılık (koşullu)"))

answers_fib.append(fib(_fnext(),
    "Her BBN düğümü, ebeveyn kombinasyonlarının her biri için olasılıkları içeren bir __________ (CPT) tablosuna sahiptir.",
    "Koşullu Olasılık Tablosu"))

answers_fib.append(fib(_fnext(),
    "BBN’in birleşik olasılık dağılımı genel formülü P(X1,...,Xn) = ∏ P(Xi | __________) şeklindedir.",
    "Parents(Xi)"))

answers_fib.append(fib(_fnext(),
    "BBN, Naive Bayes’in aksine değişkenler arası __________ durumlarını da modelleyebilir.",
    "bağımlılık"))

answers_fib.append(fib(_fnext(),
    "Kanıt E ve hipotez H için Bayes formülü: P(H|E) = P(E|H)·P(H) / __________.",
    "P(E)"))

answers_fib.append(fib(_fnext(),
    "BBN’de kanıt geldikten sonra olasılıkların güncellenmesine __________ (inference) denir.",
    "çıkarım"))

answers_fib.append(fib(_fnext(),
    "BBN’in temel gücü, ileri yönlü ilişki tanımlı olsa bile __________ yönlü çıkarım (sonuçtan nedene) yapabilmesidir.",
    "ters"))

answers_fib.append(fib(_fnext(),
    "BBN’in en önemli dezavantajlarından biri, değişken sayısı arttıkça CPT tablolarının __________ büyümesidir.",
    "üstel olarak"))

answers_fib.append(fib(_fnext(),
    "Bayesian Belief Network, olasılıkları hesaplamak için değil, __________ geldikten sonra doğru __________ vermek için vardır.",
    "gözlem (kanıt); kararı"))

# =====================================================================
# BÖLÜM 7 — HIDDEN MARKOV MODEL (HMM)
# =====================================================================
story.append(PageBreak())
h1("BÖLÜM 7 — Hidden Markov Model (HMM)")
h2("A. Çoktan Seçmeli Sorular")

answers_mcq.append(mcq(_next(),
    "HMM adını hangi iki bileşenden alır?",
    ["Hierarchical + Multi", "Hidden + Markov", "High + Measurement", "Heuristic + Modal", "Hybrid + Mixture"],
    1))

answers_mcq.append(mcq(_next(),
    "Markov özelliğinin temel ifadesi hangisidir?",
    ["Sistemin gelecekteki durumu, geçmişteki tüm durumlara bağlıdır",
     "Sistemin gelecekteki durumu yalnızca mevcut (şimdiki) duruma bağlıdır; geçmişe gerek yoktur",
     "Gelecek durum rastgele seçilir",
     "Sistem hiç değişmez",
     "Geçmiş ve gelecek her zaman eşittir"],
    1))

answers_mcq.append(mcq(_next(),
    "Markov Zinciri ile HMM arasındaki fark nedir?",
    ["Markov Zinciri’nde durumlar gizlidir; HMM’de gözlemlenebilir",
     "Markov Zinciri’nde durumlar doğrudan gözlenebilir; HMM’de durumlar gizlidir, sadece gözlemler görülür",
     "İkisi tamamen aynıdır",
     "HMM geçiş olasılıkları kullanmaz",
     "Markov Zinciri emisyon olasılıkları kullanır"],
    1))

answers_mcq.append(mcq(_next(),
    "HMM’in beş temel parametresi (N, Q, V, π, A, B) arasında ‘B’ (veya E) hangisini ifade eder?",
    ["Durum sayısı",
     "Başlangıç olasılıkları",
     "Geçiş olasılıkları",
     "Emisyon olasılıkları (bir durumdayken belirli bir gözlemin üretilme olasılığı)",
     "Gözlem dizisinin uzunluğu"],
    3))

answers_mcq.append(mcq(_next(),
    "π (başlangıç olasılıkları) hangi koşulu sağlamak zorundadır?",
    ["Tümü 0 olmalıdır",
     "Toplamları 1 olmalıdır",
     "Birbirlerine eşit olmalıdır",
     "Negatif olabilir",
     "Yalnızca geçiş matrisine bağlıdır"],
    1))

answers_mcq.append(mcq(_next(),
    "Geçiş matrisi A’nın satır toplamı kaç olmalıdır?",
    ["0", "1", "−1", "Durum sayısı N kadar", "Gözlem sayısı kadar"],
    1))

answers_mcq.append(mcq(_next(),
    "Emisyon matrisi B’nin satırları neyi temsil eder ve satır toplamları kaç olmalıdır?",
    ["Gözlemleri — toplam 0",
     "Durumları — toplam 1 (her durum için emisyon olasılıkları toplamı 1)",
     "Zaman adımlarını — toplam N",
     "Etiketleri — toplam T",
     "Başlangıç olasılıklarını — toplam 0"],
    1))

answers_mcq.append(mcq(_next(),
    "HMM’in üç temel problemi hangileridir?",
    ["Sıralama, kümeleme, regresyon",
     "Değerlendirme (Evaluation), Çözümleme (Decoding), Öğrenme (Learning)",
     "Normalize etme, segmentasyon, son-işleme",
     "Eğitim, test, doğrulama",
     "Özellik seçimi, veri temizleme, raporlama"],
    1))

answers_mcq.append(mcq(_next(),
    "Forward algoritması hangi problemi çözer?",
    ["Decoding",
     "Öğrenme",
     "Evaluation (gözlem dizisinin modelden gelme olasılığı P(O|model))",
     "Kümeleme",
     "Bellek yönetimi"],
    2))

answers_mcq.append(mcq(_next(),
    "Viterbi algoritması hangi problemi çözer ve Forward ile temel farkı nedir?",
    ["Evaluation; TOPLAM yerine MAX kullanır",
     "Öğrenme; EM uygular",
     "Decoding; gözlemleri en iyi açıklayan en olası gizli durum dizisini bulur, Forward’daki TOPLAM yerine MAX işlemi yapar ve backpointer tutar",
     "Kümeleme; Öklid mesafesi kullanır",
     "Normalizasyon; z-score uygular"],
    2))

answers_mcq.append(mcq(_next(),
    "Baum-Welch algoritması hangi problemi çözer?",
    ["Decoding",
     "Evaluation",
     "Learning — etiket yokken gözlem dizilerinden A, B, π parametrelerini öğrenir",
     "Kümeleme",
     "Sınıflandırma"],
    2))

answers_mcq.append(mcq(_next(),
    "Baum-Welch aslında hangi genel yöntemin HMM’e uyarlanmış biçimidir?",
    ["Gradient boosting",
     "Beklenti-Maksimizasyon (EM)",
     "k-ortalamalar",
     "DBSCAN",
     "Principal Component Analysis"],
    1))

answers_mcq.append(mcq(_next(),
    "Viterbi algoritması neden backpointer (bt) tutar?",
    ["Olasılıkları daha doğru hesaplamak için",
     "En iyi yolu geriye doğru takip edip gizli durum dizisini yeniden inşa edebilmek için",
     "Belleği artırmak için",
     "Geçiş matrisini değiştirmek için",
     "Emisyon olasılıklarını sıfırlamak için"],
    1))

answers_mcq.append(mcq(_next(),
    "Aşağıdakilerden hangisi HMM’in tipik bir uygulaması <b>değildir</b>?",
    ["Konuşma tanıma",
     "DNA dizi analizi",
     "Sözcük türü etiketleme (POS tagging)",
     "Robot konumlandırma",
     "Statik görüntü renk histogramı çıkarma"],
    4))

answers_mcq.append(mcq(_next(),
    "HMM’in sınırlılıklarından <b>olmayan</b> hangisidir?",
    ["Durum sayısının önceden belirlenmesi gerekir",
     "Uzun vadeli bağımlılıklarda LSTM/Transformer gibi derin öğrenme modellerine göre zayıf kalabilir",
     "Baum-Welch yerel optimuma takılabilir",
     "Baum-Welch global optimumu garanti eder",
     "Başlangıç değerlerine duyarlıdır"],
    3))

answers_mcq.append(mcq(_next(),
    "Forward algoritmasında αt(j) ne anlama gelir?",
    ["t anına kadar gelen tüm gözlemleri görmüş ve t anında j durumunda olma olasılığı",
     "t anına kadar gidilebilecek en yüksek olasılıklı tek yolun değeri",
     "Bir durumun entropisi",
     "Başlangıç olasılığı",
     "Geçiş matrisinin determinantı"],
    0))

answers_mcq.append(mcq(_next(),
    "Viterbi’de vt(j) Forward’daki αt(j)’den farklı olarak neyi taşır?",
    ["Tüm yolların toplamını",
     "t anına kadar olan en yüksek olasılıklı TEK yolun değerini",
     "Ortalama yol uzunluğunu",
     "Başlangıç olasılığını",
     "Gözlem sayısını"],
    1))

answers_mcq.append(mcq(_next(),
    "Pratik olarak Viterbi’de log-uzayda (log-space) çalışmanın temel nedeni nedir?",
    ["Belleği azaltmak",
     "Küçük olasılıkların çarpımının underflow’a düşmesini önleyerek sayısal kararlılık sağlamak",
     "Algoritmayı yavaşlatmak",
     "Etiketleri sıkıştırmak",
     "Veriyi silmek"],
    1))

answers_mcq.append(mcq(_next(),
    "Dondurma örneği (HOT/COLD) için Viterbi algoritması hangi soruyu cevaplar?",
    ["Tüm olası hava dizilerinin toplam olasılığını",
     "Gözlemlenen dondurma tüketim dizisini en iyi açıklayan en olası HOT/COLD dizisini",
     "Havanın rastgele simülasyonunu",
     "Yalnızca ortalama tüketimi",
     "Yalnızca entropiyi"],
    1))

answers_mcq.append(mcq(_next(),
    "HMM’in avantajlarından hangisi <b>yanlıştır</b>?",
    ["Belirsizliği modelleyebilir",
     "Ardışık veriler için doğal bir yapıdır",
     "Forward/Viterbi/Baum-Welch algoritmaları matematiksel olarak iyi tanımlıdır",
     "Baum-Welch ile etiketsiz veriden parametreler öğrenilebilir",
     "Uzun vadeli bağımlılıkları Transformer’lardan daha iyi yakalar"],
    4))

h2("B. Boşluk Doldurmalı Sorular")

answers_fib.append(fib(_fnext(),
    "Markov özelliği: Bir sistemin gelecekteki durumu yalnızca __________ duruma bağlıdır.",
    "mevcut (şimdiki)"))

answers_fib.append(fib(_fnext(),
    "HMM’de durumlar __________, gözlemler ise __________ olan bir modeldir.",
    "gizli (hidden); gözlemlenebilir"))

answers_fib.append(fib(_fnext(),
    "HMM beş parametre ile tanımlanır: durum sayısı N, durum kümesi Q, gözlem kümesi V, __________ olasılıkları π, __________ matrisi A ve __________ matrisi B.",
    "başlangıç; geçiş; emisyon"))

answers_fib.append(fib(_fnext(),
    "Geçiş matrisinde her satırın toplamı __________, emisyon matrisinde her satırın toplamı __________ olmalıdır.",
    "1; 1"))

answers_fib.append(fib(_fnext(),
    "HMM’in üç temel problemi: 1) __________ (Forward), 2) __________ (Viterbi), 3) __________ (Baum-Welch).",
    "Değerlendirme (Evaluation); Çözümleme (Decoding); Öğrenme (Learning)"))

answers_fib.append(fib(_fnext(),
    "__________ algoritması, bir gözlem dizisinin modelden gelme olasılığını P(O|model) dinamik programlama ile verimli biçimde hesaplar.",
    "Forward"))

answers_fib.append(fib(_fnext(),
    "__________ algoritması en yüksek olasılıklı tek yolu bulmak için TOPLAM yerine __________ operatörünü kullanır ve bir __________ (geri gösterici) tutar.",
    "Viterbi; MAX; backpointer"))

answers_fib.append(fib(_fnext(),
    "__________ algoritması, EM yönteminin HMM’e özel uyarlamasıdır ve etiketsiz veri üzerinden A, B, π parametrelerini öğrenir.",
    "Baum-Welch"))

answers_fib.append(fib(_fnext(),
    "Baum-Welch global optimumu garanti __________; pratikte iyi sonuç verse de __________ değerlerine duyarlıdır.",
    "etmez; başlangıç"))

answers_fib.append(fib(_fnext(),
    "HMM, özellikle __________ tanıma, __________ tanıma, DNA dizi analizi ve robot konumlandırma gibi ardışık veri problemlerinde yaygın olarak kullanılır.",
    "konuşma; el yazısı (handwriting) / POS etiketleme"))

# =====================================================================
# GENEL / KARMA SORULAR
# =====================================================================
story.append(PageBreak())
h1("BÖLÜM 8 — Genel / Konular Arası Karma Sorular")
h2("A. Çoktan Seçmeli Sorular")

answers_mcq.append(mcq(_next(),
    "Aşağıdaki yöntem–konu eşleştirmelerinden hangisi <b>yanlıştır</b>?",
    ["MLE — parametre tahmini",
     "Bayesian Kestirim — önsel ile veriyi birleştirme",
     "Parzen Pencereleri — parametrik yoğunluk kestirimi",
     "k-NN — parametrik olmayan sınıflandırma",
     "GMM — EM ile karışım parametre öğrenme"],
    2))

answers_mcq.append(mcq(_next(),
    "Aşağıdakilerden hangi ikili <b>doğru</b> bir “problem–algoritma” eşleştirmesidir?",
    ["HMM Decoding — Baum-Welch",
     "HMM Evaluation — Viterbi",
     "HMM Learning — Forward",
     "HMM Decoding — Viterbi",
     "HMM Evaluation — EM"],
    3))

answers_mcq.append(mcq(_next(),
    "Aşağıdaki yöntemlerden hangisi <b>parametrik olmayan</b> bir yöntem değildir?",
    ["Histogram yoğunluk kestirimi",
     "Parzen pencereleri",
     "k-NN yoğunluk kestirimi",
     "Gaussian kernel KDE",
     "MLE ile Gauss parametre tahmini"],
    4))

answers_mcq.append(mcq(_next(),
    "Aşağıdakilerden hangisi “az veri, çok belirsizlik” durumunda en uygun yaklaşımdır?",
    ["MLE — eldeki tek noktaya güveniriz",
     "Bayesian kestirim — önsel bilgi veriyle birleştirilir",
     "Yalnızca k-NN — k = n seçilerek",
     "Histogram — çok ince kutularla",
     "Her zaman derin öğrenme"],
    1))

answers_mcq.append(mcq(_next(),
    "Aşağıdakilerden hangi ifade “yanlılık-varyans (bias-variance) dengesi” ile <b>uyumludur</b>?",
    ["Çok büyük bant genişliği h → yüksek yanlılık, düşük varyans",
     "Çok küçük bant genişliği h → yüksek yanlılık, düşük varyans",
     "h hiç etki etmez",
     "Büyük h her zaman daha iyidir",
     "Küçük h daima düşük yanlılık ve düşük varyans verir"],
    0))

answers_mcq.append(mcq(_next(),
    "Aşağıdakilerden hangisi model seçiminde (model selection) kullanılan bir yaklaşım <b>değildir</b>?",
    ["Aday modelleri deneme ve doğrulama (validation) ile karşılaştırma",
     "Çapraz doğrulama (cross-validation)",
     "Farklı hiperparametre değerleri deneme",
     "Modeli test verisine bakarak seçmek (test verisine bakarak hiperparametre ayarlamak)",
     "Bias-variance dengesine dikkat etme"],
    3,
    "Test verisine bakarak hiperparametre seçmek veri sızıntısıdır."))

answers_mcq.append(mcq(_next(),
    "Aşağıdaki ifadelerden hangisi <b>doğrudur</b>?",
    ["Bayes sınıflandırıcısı dağılımlar bilindiğinde ulaşılabilecek en düşük hata oranını (Bayes hatası) verir",
     "Bayes sınıflandırıcısı her zaman sıfır hata verir",
     "Parzen yöntemi her zaman k-NN’den daha iyidir",
     "k-NN yalnızca düşük boyutta çalışır",
     "HMM yalnızca iki durumla kullanılır"],
    0))

answers_mcq.append(mcq(_next(),
    "Bayesian Belief Network ile Hidden Markov Model arasındaki benzerlik nedir?",
    ["İkisi de olasılıksal grafik modellerdir; koşullu bağımlılıkları modelleyerek belirsizlik altında karar/çıkarım yaparlar",
     "İkisi de yalnızca sürekli değişkenlerle çalışır",
     "İkisi de k-NN tabanlıdır",
     "İkisi de etiket gerektirmez",
     "İkisi de tamamen aynıdır"],
    0))

answers_mcq.append(mcq(_next(),
    "GMM ile Parzen pencereleri arasındaki temel fark nedir?",
    ["GMM parametrik (sabit sayıda bileşen), Parzen parametrik olmayan (her veri noktası bir katkı) yöntemdir",
     "İkisi de parametrik olmayan yöntemlerdir",
     "GMM etiket gerektirir, Parzen gerektirmez",
     "Parzen yalnızca tek boyutta tanımlıdır",
     "GMM bir sınıflandırma algoritmasıdır, yoğunlukla ilgisi yoktur"],
    0))

answers_mcq.append(mcq(_next(),
    "Tıbbi tanı gibi asimetrik maliyete sahip bir problemde en uygun karar kuralı nedir?",
    ["Sadece maksimum olabilirlik",
     "MAP — sonsalı maksimize et",
     "Minimum risk Bayes kuralı (kayıp fonksiyonunu hesaba katan)",
     "k-NN voting — eşit maliyet varsayarak",
     "Histogram eşik"],
    2))

h2("B. Boşluk Doldurmalı Sorular")

answers_fib.append(fib(_fnext(),
    "Modelin karmaşıklığı arttıkça eğitim hatası __________; ancak test hatası önce düşer sonra __________, bu bölgeye __________ bölgesi denir.",
    "azalır; artar; aşırı öğrenme (overfitting)"))

answers_fib.append(fib(_fnext(),
    "Bayes sınıflandırıcısı, dağılımlar bilindiğinde elde edilebilecek en düşük hata oranı olan __________ hatasını tanımlar.",
    "Bayes"))

answers_fib.append(fib(_fnext(),
    "Parametrik yöntemlerde dağılım formu varsayılır ve __________ tahmin edilir; parametrik olmayan yöntemlerde ise dağılım formu hakkında __________ yapılmaz.",
    "parametreler; varsayım"))

answers_fib.append(fib(_fnext(),
    "Makine algısında karar sürecini iyileştirmek için kullanılan, girdi dışındaki ek bilgi olan __________ ile maliyet/risk __________ birleştirilir.",
    "bağlam (context); ayarlaması"))

answers_fib.append(fib(_fnext(),
    "Forward algoritması tüm yolların __________ ile P(O|model) verirken, Viterbi algoritması tek yolun __________ değeriyle en olası gizli durum dizisini verir.",
    "toplamı; maksimumu"))

answers_fib.append(fib(_fnext(),
    "BBN ve HMM, her ikisi de koşullu bağımlılıkları modelleyen __________ grafik modellerdir.",
    "olasılıksal (probabilistic)"))

answers_fib.append(fib(_fnext(),
    "Etiketsiz verilerle parametre öğrenirken GMM’de __________ algoritması, HMM’de ise __________ algoritması kullanılır.",
    "EM; Baum-Welch"))

answers_fib.append(fib(_fnext(),
    "Parzen’de __________ seçimi, k-NN’de ise __________ seçimi kritik hiperparametredir.",
    "bant genişliği h; komşu sayısı k"))

answers_fib.append(fib(_fnext(),
    "Boyutluluk laneti, veri sayısı sabitken özellik sayısı arttıkça veri noktalarının uzayda __________ hale gelmesidir; bu da tahmini __________ yapar.",
    "seyrek; güvenilmez"))

answers_fib.append(fib(_fnext(),
    "Bayes karar teorisinde sıfır-bir kayıp kullanıldığında karar kuralı, her x için __________ olasılığı en yüksek sınıfı seçmeye indirgenir ve buna __________ kuralı denir.",
    "sonsal (posterior); MAP (Maximum A Posteriori)"))

# =====================================================================
# ANSWER KEY
# =====================================================================
story.append(PageBreak())
h1("CEVAP ANAHTARI (Answer Key)")

h2("A. Çoktan Seçmeli (MCQ) Cevapları")

# Build a nicely formatted answer key with 4 per line
from reportlab.platypus import Table, TableStyle

rows = []
row = []
for i, (n, letter, _) in enumerate(answers_mcq, 1):
    row.append(f"{n}) {letter}")
    if len(row) == 5:
        rows.append(row)
        row = []
if row:
    while len(row) < 5:
        row.append("")
    rows.append(row)

t = Table(rows, colWidths=[3.3 * cm] * 5)
t.setStyle(TableStyle([
    ("FONT", (0, 0), (-1, -1), "ArialU", 10),
    ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1a365d")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e0")),
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7fafc")),
]))
story.append(t)
story.append(Spacer(1, 14))

h2("B. Boşluk Doldurmalı (FIB) Cevapları")

for n, ans, _ in answers_fib:
    story.append(Paragraph(f"<b>{n}.</b> {ans}", ans_style))

h2("C. Açıklamalı MCQ Notları (Seçilmiş Sorular)")
for n, letter, exp in answers_mcq:
    if exp:
        story.append(Paragraph(f"<b>Soru {n} ({letter}):</b> {exp}", note_style))

# ---------- BUILD ----------
doc = SimpleDocTemplate(
    "Pattern_Recognition_Vize_Soru_Bankasi.pdf",
    pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm,
    topMargin=1.8 * cm, bottomMargin=1.8 * cm,
    title="Örüntü Tanıma - Vize Soru Bankası",
    author="BLM0462",
)


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("ArialU", 8)
    canvas.setFillColor(colors.HexColor("#718096"))
    canvas.drawRightString(
        A4[0] - 2 * cm, 1.1 * cm,
        f"Sayfa {doc.page}"
    )
    canvas.drawString(
        2 * cm, 1.1 * cm,
        "BLM0462 Örüntü Tanıma — Vize Soru Bankası"
    )
    canvas.restoreState()


doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF oluşturuldu. Toplam MCQ: {len(answers_mcq)}, Toplam FIB: {len(answers_fib)}")

# ---------- Web quiz JSON ----------
WEB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz-web")
os.makedirs(WEB_DIR, exist_ok=True)
quiz_payload = {
    "title": "BLM0462 Örüntü Tanıma — Vize Soru Bankası",
    "subtitle": "Çoktan seçmeli ve boşluk doldurma — cevapları kontrol edin",
    "mcq": quiz_mcq_data,
    "fib": quiz_fib_data,
}
json_path = os.path.join(WEB_DIR, "questions.json")
with open(json_path, "w", encoding="utf-8") as jf:
    json.dump(quiz_payload, jf, ensure_ascii=False, indent=2)
print(f"Web quiz verisi yazıldı: {json_path}")

# file:// ile açıldığında fetch engellenebileceği için JS modülü de üret
js_path = os.path.join(WEB_DIR, "questions-data.js")
with open(js_path, "w", encoding="utf-8") as jf:
    jf.write("window.QUIZ_DATA = ")
    json.dump(quiz_payload, jf, ensure_ascii=False)
    jf.write(";\n")
print(f"Web quiz JS verisi yazıldı: {js_path}")
