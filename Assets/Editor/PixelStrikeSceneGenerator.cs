#if UNITY_EDITOR
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using System.IO;

namespace PixelStrike.EditorTools
{
    public static class PixelStrikeSceneGenerator
    {
        private const string SceneFolder = "Assets/Scenes";

        [MenuItem("PIXEL STRIKE/Generate Base Scenes")]
        public static void GenerateBaseScenes()
        {
            if (!Directory.Exists(SceneFolder))
                Directory.CreateDirectory(SceneFolder);

            CreateBootScene();
            CreateMainMenuScene();
            CreateTrainingScene();

            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();

            Debug.Log("PIXEL STRIKE: базовые сцены созданы.");
        }

        private static void CreateBootScene()
        {
            Scene scene = EditorSceneManager.NewScene(
                NewSceneSetup.EmptyScene,
                NewSceneMode.Single
            );

            GameObject boot = new GameObject("Boot");
            boot.AddComponent<GameBootstrap>();

            SaveScene(scene, "Boot");
        }

        private static void CreateMainMenuScene()
        {
            Scene scene = EditorSceneManager.NewScene(
                NewSceneSetup.DefaultGameObjects,
                NewSceneMode.Single
            );

            GameObject canvasObject = new GameObject(
                "MainMenuCanvas",
                typeof(Canvas),
                typeof(CanvasScaler),
                typeof(GraphicRaycaster)
            );

            Canvas canvas = canvasObject.GetComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;

            CanvasScaler scaler = canvasObject.GetComponent<CanvasScaler>();
            scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
            scaler.referenceResolution = new Vector2(1080, 1920);

            GameObject title = CreateText(
                canvasObject.transform,
                "PIXEL STRIKE",
                new Vector2(0, 0.25f),
                64
            );

            GameObject play = CreateButton(
                canvasObject.transform,
                "PLAY",
                new Vector2(0, 0)
            );

            GameObject settings = CreateButton(
                canvasObject.transform,
                "SETTINGS",
                new Vector2(0, -120)
            );

            GameObject controller = new GameObject("MainMenuController");
            var menu = controller.AddComponent<PixelStrike.UI.MainMenuController>();

            // Кнопки будут подключены вручную в Inspector,
            // чтобы не зависеть от неизвестных имён полей скрипта.
            play.name = "PlayButton";
            settings.name = "SettingsButton";

            SaveScene(scene, "MainMenu");
        }

        private static void CreateTrainingScene()
        {
            Scene scene = EditorSceneManager.NewScene(
                NewSceneSetup.DefaultGameObjects,
                NewSceneMode.Single
            );

            GameObject floor = GameObject.CreatePrimitive(PrimitiveType.Cube);
            floor.name = "TrainingFloor";
            floor.transform.position = new Vector3(0, -0.5f, 0);
            floor.transform.localScale = new Vector3(30, 1, 30);

            GameObject light = new GameObject("TrainingLight");
            var sun = light.AddComponent<Light>();
            sun.type = LightType.Directional;
            light.transform.rotation = Quaternion.Euler(50, -30, 0);

            GameObject marker = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            marker.name = "TrainingTarget";
            marker.transform.position = new Vector3(0, 1, 8);

            SaveScene(scene, "Training");
        }

        private static GameObject CreateText(
            Transform parent, string value, Vector2 anchor, int fontSize)
        {
            GameObject obj = new GameObject(
                value,
                typeof(RectTransform),
                typeof(CanvasRenderer),
                typeof(Text)
            );

            obj.transform.SetParent(parent, false);

            RectTransform rect = obj.GetComponent<RectTransform>();
            rect.anchorMin = new Vector2(0.1f, 0.5f);
            rect.anchorMax = new Vector2(0.9f, 0.5f);
            rect.pivot = new Vector2(0.5f, 0.5f);
            rect.anchoredPosition = anchor;
            rect.sizeDelta = new Vector2(0, 100);

            Text text = obj.GetComponent<Text>();
            text.text = value;
            text.alignment = TextAnchor.MiddleCenter;
            text.fontSize = fontSize;
            text.color = Color.white;
            text.font = Resources.GetBuiltinResource<Font>("Arial.ttf");

            return obj;
        }

        private static GameObject CreateButton(
            Transform parent, string label, Vector2 position)
        {
            GameObject obj = new GameObject(
                label,
                typeof(RectTransform),
                typeof(CanvasRenderer),
                typeof(Image),
                typeof(Button)
            );

            obj.transform.SetParent(parent, false);

            RectTransform rect = obj.GetComponent<RectTransform>();
            rect.anchorMin = new Vector2(0.2f, 0.5f);
            rect.anchorMax = new Vector2(0.8f, 0.5f);
            rect.pivot = new Vector2(0.5f, 0.5f);
            rect.anchoredPosition = position;
            rect.sizeDelta = new Vector2(0, 90);

            Image image = obj.GetComponent<Image>();
            image.color = new Color(0.12f, 0.45f, 0.85f, 1f);

            CreateText(obj.transform, label, Vector2.zero, 30);

            return obj;
        }

        private static void SaveScene(Scene scene, string name)
        {
            string path = $"{SceneFolder}/{name}.unity";
            EditorSceneManager.SaveScene(scene, path);
        }
    }
}
#endif
