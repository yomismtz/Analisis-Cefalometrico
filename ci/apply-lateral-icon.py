from pathlib import Path
import shutil

ROOT = Path(".")
drawable = ROOT / "app/src/main/res/drawable"
mipmap = ROOT / "app/src/main/res/mipmap-anydpi"
drawable.mkdir(parents=True, exist_ok=True)
mipmap.mkdir(parents=True, exist_ok=True)

foreground = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="@android:color/transparent" android:strokeColor="#FFFFFF" android:strokeWidth="3.4" android:strokeLineCap="round" android:strokeLineJoin="round" android:pathData="M43,20 C56,17 69,23 74,34 C77,40 76,46 73,51 L80,54 L74,59 L74,65 L68,67 L68,75 L57,79 C48,77 42,70 40,61 C38,51 39,40 41,31 C42,26 42,23 43,20" />
    <path android:fillColor="#B9F3E6" android:pathData="M52,38 A3,3 0,1 0,58,38 A3,3 0,1 0,52,38" />
    <path android:fillColor="@android:color/transparent" android:strokeColor="#22BFC7" android:strokeWidth="2.5" android:strokeLineCap="round" android:pathData="M70,53 L61,54 L56,61" />
    <path android:fillColor="@android:color/transparent" android:strokeColor="#22BFC7" android:strokeWidth="3.8" android:strokeLineCap="round" android:strokeLineJoin="round" android:pathData="M24,83 L82,83 L82,39 Z" />
    <path android:fillColor="@android:color/transparent" android:strokeColor="#B9F3E6" android:strokeWidth="2" android:strokeLineCap="round" android:pathData="M34,75 L70,75 M44,67 L70,67 M54,59 L70,59" />
    <path android:fillColor="#FFFFFF" android:pathData="M40,28 A2.4,2.4 0,1 0,44.8,28 A2.4,2.4 0,1 0,40,28 M51,38 A2.4,2.4 0,1 0,55.8,38 A2.4,2.4 0,1 0,51,38 M59,54 A2.4,2.4 0,1 0,63.8,54 A2.4,2.4 0,1 0,59,54 M56,69 A2.4,2.4 0,1 0,60.8,69 A2.4,2.4 0,1 0,56,69" />
</vector>
"""

mark = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#6842B8" android:pathData="M20,8 L88,8 C95,8 100,13 100,20 L100,88 C100,95 95,100 88,100 L20,100 C13,100 8,95 8,88 L8,20 C8,13 13,8 20,8 Z" />
    <path android:fillColor="@android:color/transparent" android:strokeColor="#FFFFFF" android:strokeWidth="3.4" android:strokeLineCap="round" android:strokeLineJoin="round" android:pathData="M43,20 C56,17 69,23 74,34 C77,40 76,46 73,51 L80,54 L74,59 L74,65 L68,67 L68,75 L57,79 C48,77 42,70 40,61 C38,51 39,40 41,31 C42,26 42,23 43,20" />
    <path android:fillColor="#B9F3E6" android:pathData="M52,38 A3,3 0,1 0,58,38 A3,3 0,1 0,52,38" />
    <path android:fillColor="@android:color/transparent" android:strokeColor="#22BFC7" android:strokeWidth="2.5" android:strokeLineCap="round" android:pathData="M70,53 L61,54 L56,61" />
    <path android:fillColor="@android:color/transparent" android:strokeColor="#22BFC7" android:strokeWidth="3.8" android:strokeLineCap="round" android:strokeLineJoin="round" android:pathData="M24,83 L82,83 L82,39 Z" />
    <path android:fillColor="@android:color/transparent" android:strokeColor="#B9F3E6" android:strokeWidth="2" android:strokeLineCap="round" android:pathData="M34,75 L70,75 M44,67 L70,67 M54,59 L70,59" />
</vector>
"""

(drawable / "ic_yomceph_foreground.xml").write_text(foreground, encoding="utf-8")
(drawable / "ic_yomceph_mark.xml").write_text(mark, encoding="utf-8")
shutil.copyfile(drawable / "ic_yomceph_mark.xml", mipmap / "ic_launcher.xml")
print("Standalone lateral launcher icon applied.")
