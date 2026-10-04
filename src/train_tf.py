from pathlib import Path
import tensorflow as tf

BASE_DIR = Path(__file__).resolve().parent.parent
TRAIN_DIR = BASE_DIR / "data" / "split" / "train"
VAL_DIR = BASE_DIR / "data" / "split" / "val"
OUT_DIR = BASE_DIR / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH = 16
EPOCHS = 10

def main():
    if not TRAIN_DIR.exists() or not VAL_DIR.exists():
        raise FileNotFoundError("Folder split belum ada. Jalankan split_dataset.py dulu.")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        TRAIN_DIR, image_size=IMG_SIZE, batch_size=BATCH, label_mode="int", shuffle=True
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        VAL_DIR, image_size=IMG_SIZE, batch_size=BATCH, label_mode="int", shuffle=False
    )

    class_names = train_ds.class_names
    (OUT_DIR / "class_names.txt").write_text("\n".join(class_names), encoding="utf-8")

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(AUTOTUNE)
    val_ds = val_ds.prefetch(AUTOTUNE)

    data_aug = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.05),
        tf.keras.layers.RandomZoom(0.1),
    ])

    base = tf.keras.applications.MobileNetV2(
        input_shape=IMG_SIZE + (3,),
        include_top=False,
        weights="imagenet"
    )
    base.trainable = False

    inputs = tf.keras.Input(shape=IMG_SIZE + (3,))
    x = data_aug(inputs)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    x = base(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = tf.keras.layers.Dense(len(class_names), activation="softmax")(x)

    model = tf.keras.Model(inputs, outputs)
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])

    ckpt = OUT_DIR / "best.keras"
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(str(ckpt), save_best_only=True, monitor="val_accuracy", mode="max"),
        tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True, monitor="val_accuracy", mode="max")
    ]

    model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS, callbacks=callbacks)

    final_path = OUT_DIR / "model_food.keras"
    model.save(final_path)
    print("✅ Model disimpan:", final_path)
    print("✅ Class names:", OUT_DIR / "class_names.txt")

if __name__ == "__main__":
    main()
