from pathlib import Path
import random
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
SPLIT_DIR = BASE_DIR / "data" / "split"
TRAIN_DIR = SPLIT_DIR / "train"
VAL_DIR = SPLIT_DIR / "val"

IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

def is_image(p: Path) -> bool:
    return p.suffix.lower() in IMG_EXT

def main(val_ratio=0.2, seed=42):
    if not RAW_DIR.exists():
        raise FileNotFoundError(f"RAW_DIR tidak ada: {RAW_DIR}")

    random.seed(seed)

    # hapus split lama (biar bersih)
    if SPLIT_DIR.exists():
        shutil.rmtree(SPLIT_DIR)

    TRAIN_DIR.mkdir(parents=True, exist_ok=True)
    VAL_DIR.mkdir(parents=True, exist_ok=True)

    classes = sorted([d for d in RAW_DIR.iterdir() if d.is_dir()], key=lambda x: x.name.lower())

    for cdir in classes:
        imgs = [p for p in cdir.iterdir() if p.is_file() and is_image(p)]
        if len(imgs) < 2:
            print(f"[SKIP] {cdir.name} gambar terlalu sedikit: {len(imgs)}")
            continue

        random.shuffle(imgs)
        n_val = max(1, int(len(imgs) * val_ratio))

        val_imgs = imgs[:n_val]
        train_imgs = imgs[n_val:]

        out_train = TRAIN_DIR / cdir.name
        out_val = VAL_DIR / cdir.name
        out_train.mkdir(parents=True, exist_ok=True)
        out_val.mkdir(parents=True, exist_ok=True)

        for p in train_imgs:
            shutil.copy2(p, out_train / p.name)
        for p in val_imgs:
            shutil.copy2(p, out_val / p.name)

        print(f"[OK] {cdir.name}: train={len(train_imgs)} val={len(val_imgs)}")

    print("\n✅ Split selesai di:", SPLIT_DIR)

if __name__ == "__main__":
    main(val_ratio=0.2)
