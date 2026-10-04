# import os
# import numpy as np
# import streamlit as st
# from PIL import Image

# import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras import layers, models
# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# from streamlit_cropper import st_cropper

# # =====================
# # PATH
# # =====================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# TRAIN_DIR = os.path.join(BASE_DIR, "dataset", "train")
# VAL_DIR = os.path.join(BASE_DIR, "dataset", "val")
# OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# BEST_MODEL_PATH = os.path.join(OUTPUT_DIR, "best_model.keras")
# FINAL_MODEL_PATH = os.path.join(OUTPUT_DIR, "final_model.keras")

# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # =====================
# # CONFIG
# # =====================
# IMG_SIZE = (224, 224)
# EPOCHS_DEFAULT = 30

# st.set_page_config(page_title="Food Recognition", layout="centered")
# st.title("🍽️ Food Recognition — Train + Predict (Streamlit + Cropper)")

# # =====================
# # HELPERS
# # =====================
# def list_classes_from_train():
#     if not os.path.isdir(TRAIN_DIR):
#         return []
#     return sorted([
#         d for d in os.listdir(TRAIN_DIR)
#         if os.path.isdir(os.path.join(TRAIN_DIR, d))
#     ])

# def folders_exist_train_val():
#     return os.path.isdir(TRAIN_DIR) and os.path.isdir(VAL_DIR)

# def model_file_ok(path: str) -> bool:
#     return os.path.exists(path) and os.path.getsize(path) > 50_000  # anti file kosong/korup

# def build_model(num_classes: int):
#     model = models.Sequential([
#         layers.Conv2D(32, (3,3), activation="relu", input_shape=(224,224,3)),
#         layers.MaxPooling2D(2,2),
#         layers.Conv2D(64, (3,3), activation="relu"),
#         layers.MaxPooling2D(2,2),
#         layers.Conv2D(128, (3,3), activation="relu"),
#         layers.MaxPooling2D(2,2),
#         layers.Flatten(),
#         layers.Dense(128, activation="relu"),
#         layers.Dense(num_classes, activation="softmax")
#     ])
#     model.compile(
#         optimizer="adam",
#         loss="categorical_crossentropy",
#         metrics=["accuracy"]
#     )
#     return model

# def preprocess_image(pil_img: Image.Image):
#     pil_img = pil_img.convert("RGB").resize(IMG_SIZE)
#     arr = np.array(pil_img).astype("float32") / 255.0
#     arr = np.expand_dims(arr, axis=0)
#     return arr

# @st.cache_resource
# def load_model_cached(model_path: str):
#     return tf.keras.models.load_model(model_path)

# # =====================
# # SIDEBAR
# # =====================
# mode = st.sidebar.radio("Mode", ["Predict (Upload Gambar)", "Train Model"])

# st.sidebar.markdown("### Status model")
# st.sidebar.write("Best:", "✅" if model_file_ok(BEST_MODEL_PATH) else "❌")
# st.sidebar.write("Final:", "✅" if model_file_ok(FINAL_MODEL_PATH) else "❌")

# st.sidebar.markdown("### Path")
# st.sidebar.write("Train:", TRAIN_DIR)
# st.sidebar.write("Val:", VAL_DIR)
# st.sidebar.write("Output:", OUTPUT_DIR)

# # =====================
# # PREDICT MODE
# # =====================
# if mode == "Predict (Upload Gambar)":
#     st.subheader("🔎 Prediksi dari Gambar")

#     classes = list_classes_from_train()
#     if len(classes) == 0:
#         st.warning("Folder dataset/train belum ada / belum berisi kelas. Buat dulu struktur dataset.")
#         st.stop()

#     model_choice_label = st.selectbox(
#         "Pilih model",
#         options=[
#             "Best Model (output/best_model.keras)",
#             "Final Model (output/final_model.keras)",
#         ],
#         index=0
#     )
#     model_path = BEST_MODEL_PATH if "Best" in model_choice_label else FINAL_MODEL_PATH

#     if not model_file_ok(model_path):
#         st.warning("Model belum valid / belum ada. Silakan training dulu di mode **Train Model**.")
#         st.stop()

#     uploaded = st.file_uploader("Upload gambar (jpg/png)", type=["jpg", "jpeg", "png"])

#     if uploaded is not None:
#         img = Image.open(uploaded)

#         st.markdown("### 🖼️ Gambar Asli vs ✂️ Hasil Crop")
#         col1, col2 = st.columns(2)

#         with col1:
#             st.image(img, caption="Gambar Asli", use_container_width=True)

#         with col2:
#             cropped_img = st_cropper(
#                 img,
#                 realtime_update=True,
#                 box_color="#00FFAA",
#                 aspect_ratio=(1, 1)  # ubah jadi None kalau mau bebas
#             )
#             st.image(cropped_img, caption="Hasil Crop", use_container_width=True)

#         st.markdown("---")

#         if st.button("🔍 Predict"):
#             x = preprocess_image(cropped_img)

#             model = load_model_cached(model_path)
#             preds = model.predict(x, verbose=0)[0]

#             top_idx = int(np.argmax(preds))
#             confidence = float(preds[top_idx])

#             st.success(f"Prediksi: **{classes[top_idx]}**")
#             st.write(f"Confidence: **{confidence:.4f}**")

#             st.markdown("### Top-5")
#             top5 = np.argsort(preds)[::-1][:5]
#             for i in top5:
#                 st.write(f"- {classes[int(i)]}: {float(preds[int(i)]):.4f}")

# # =====================
# # TRAIN MODE
# # =====================
# else:
#     st.subheader("🏋️ Train Model (Train + Val)")

#     if not folders_exist_train_val():
#         st.error(
#             "Folder dataset belum lengkap.\n\n"
#             "Pastikan ada:\n"
#             "- dataset/train/<class_name>/...\n"
#             "- dataset/val/<class_name>/...\n"
#         )
#         st.stop()

#     classes = list_classes_from_train()
#     st.write("Detected classes:", classes)

#     epochs = st.number_input("Epochs", min_value=1, max_value=200, value=EPOCHS_DEFAULT, step=1)
#     batch_size = st.selectbox("Batch size", [8, 16, 32, 64], index=2)

#     st.caption("Model akan tersimpan di output/ sebagai best_model.keras dan final_model.keras")

#     if st.button("Start Training"):
#         with st.spinner("Training... (lihat log di bawah)"):
#             train_datagen = ImageDataGenerator(
#                 rescale=1./255,
#                 rotation_range=20,
#                 zoom_range=0.2,
#                 horizontal_flip=True
#             )
#             val_datagen = ImageDataGenerator(rescale=1./255)

#             train_generator = train_datagen.flow_from_directory(
#                 TRAIN_DIR,
#                 target_size=IMG_SIZE,
#                 batch_size=batch_size,
#                 class_mode="categorical",
#                 shuffle=True
#             )

#             val_generator = val_datagen.flow_from_directory(
#                 VAL_DIR,
#                 target_size=IMG_SIZE,
#                 batch_size=batch_size,
#                 class_mode="categorical",
#                 shuffle=False
#             )

#             model = build_model(train_generator.num_classes)

#             callbacks = [
#                 EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
#                 ModelCheckpoint(filepath=BEST_MODEL_PATH, monitor="val_accuracy", save_best_only=True),
#             ]

#             log_area = st.empty()
#             logs = []

#             class StreamlitCallback(tf.keras.callbacks.Callback):
#                 def on_epoch_end(self, epoch, logs_dict=None):
#                     logs_dict = logs_dict or {}
#                     msg = (
#                         f"Epoch {epoch+1}/{int(epochs)} | "
#                         f"loss={logs_dict.get('loss', 0):.4f} acc={logs_dict.get('accuracy', 0):.4f} | "
#                         f"val_loss={logs_dict.get('val_loss', 0):.4f} val_acc={logs_dict.get('val_accuracy', 0):.4f}"
#                     )
#                     logs.append(msg)
#                     log_area.text("\n".join(logs))

#             model.fit(
#                 train_generator,
#                 validation_data=val_generator,
#                 epochs=int(epochs),
#                 callbacks=callbacks + [StreamlitCallback()],
#                 verbose=0
#             )

#             model.save(FINAL_MODEL_PATH)

#         st.success("✅ Training selesai!")
#         st.write("Saved:")
#         st.write("-", BEST_MODEL_PATH)
#         st.write("-", FINAL_MODEL_PATH)
#         st.info("Sekarang pindah ke mode **Predict** untuk uji upload gambar.")
