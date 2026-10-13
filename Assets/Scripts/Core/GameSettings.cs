using UnityEngine;

public static class GameSettings
{
    private const string MusicKey = "music_volume";
    private const string SfxKey = "sfx_volume";
    private const string SensitivityKey = "look_sensitivity";
    private const string QualityKey = "graphics_quality";

    public static float MusicVolume
    {
        get => PlayerPrefs.GetFloat(MusicKey, 0.8f);
        set => PlayerPrefs.SetFloat(MusicKey, Mathf.Clamp01(value));
    }

    public static float SfxVolume
    {
        get => PlayerPrefs.GetFloat(SfxKey, 1f);
        set => PlayerPrefs.SetFloat(SfxKey, Mathf.Clamp01(value));
    }

    public static float LookSensitivity
    {
        get => PlayerPrefs.GetFloat(SensitivityKey, 1f);
        set => PlayerPrefs.SetFloat(
            SensitivityKey, Mathf.Clamp(value, 0.1f, 5f));
    }

    public static int GraphicsQuality
    {
        get => PlayerPrefs.GetInt(QualityKey, 1);
        set => PlayerPrefs.SetInt(QualityKey, Mathf.Clamp(value, 0, 2));
    }

    public static void Save()
    {
        PlayerPrefs.Save();
    }
}
