from pathlib import Path

root = Path("Assets/Scripts")

files = {
"Mobile/MobileInputState.cs": r'''
using UnityEngine;

namespace PixelStrike.Mobile
{
    public static class MobileInputState
    {
        public static Vector2 Movement;
        public static Vector2 Look;
        public static bool FirePressed;
        public static bool ReloadPressed;
        public static bool JumpPressed;

        public static void ResetFrameInput()
        {
            Look = Vector2.zero;
            ReloadPressed = false;
            JumpPressed = false;
        }

        public static void ResetAll()
        {
            Movement = Vector2.zero;
            ResetFrameInput();
            FirePressed = false;
        }
    }
}
''',
"Mobile/VirtualJoystick.cs": r'''
using UnityEngine;
using UnityEngine.EventSystems;

namespace PixelStrike.Mobile
{
    public sealed class VirtualJoystick : MonoBehaviour,
        IPointerDownHandler, IDragHandler, IPointerUpHandler
    {
        [SerializeField] private RectTransform background;
        [SerializeField] private RectTransform handle;
        [SerializeField, Range(0.1f, 1f)] private float handleRange = 0.65f;

        private Canvas canvas;
        private Camera uiCamera;

        private void Awake()
        {
            canvas = GetComponentInParent<Canvas>();
            if (canvas != null && canvas.renderMode != RenderMode.ScreenSpaceOverlay)
                uiCamera = canvas.worldCamera;
        }

        public void OnPointerDown(PointerEventData eventData) => OnDrag(eventData);

        public void OnDrag(PointerEventData eventData)
        {
            if (background == null || handle == null)
                return;

            if (!RectTransformUtility.ScreenPointToLocalPointInRectangle(
                background, eventData.position, uiCamera, out Vector2 localPoint))
                return;

            Vector2 half = background.rect.size * 0.5f;
            Vector2 normalized = new Vector2(
                half.x > 0 ? localPoint.x / half.x : 0,
                half.y > 0 ? localPoint.y / half.y : 0);

            normalized = Vector2.ClampMagnitude(normalized, 1f);
            handle.anchoredPosition = normalized * half * handleRange;
            MobileInputState.Movement = normalized;
        }

        public void OnPointerUp(PointerEventData eventData)
        {
            if (handle != null)
                handle.anchoredPosition = Vector2.zero;

            MobileInputState.Movement = Vector2.zero;
        }
    }
}
''',
"Mobile/MobileActionButton.cs": r'''
using UnityEngine;
using UnityEngine.EventSystems;

namespace PixelStrike.Mobile
{
    public enum MobileAction
    {
        Fire, Reload, Jump
    }

    public sealed class MobileActionButton : MonoBehaviour,
        IPointerDownHandler, IPointerUpHandler
    {
        [SerializeField] private MobileAction action;

        public void OnPointerDown(PointerEventData eventData)
        {
            SetAction(true);
        }

        public void OnPointerUp(PointerEventData eventData)
        {
            SetAction(false);
        }

        private void SetAction(bool pressed)
        {
            switch (action)
            {
                case MobileAction.Fire:
                    MobileInputState.FirePressed = pressed;
                    break;
                case MobileAction.Reload:
                    if (pressed) MobileInputState.ReloadPressed = true;
                    break;
                case MobileAction.Jump:
                    if (pressed) MobileInputState.JumpPressed = true;
                    break;
            }
        }

        private void OnDisable()
        {
            if (action == MobileAction.Fire)
                MobileInputState.FirePressed = false;
        }
    }
}
''',
"Player/PlayerMovementController.cs": r'''
using UnityEngine;
using PixelStrike.Mobile;

namespace PixelStrike.Player
{
    [RequireComponent(typeof(CharacterController))]
    public sealed class PlayerMovementController : MonoBehaviour
    {
        [SerializeField] private Transform cameraTransform;
        [SerializeField] private float moveSpeed = 5f;
        [SerializeField] private float gravity = -20f;
        [SerializeField] private float jumpHeight = 1.2f;

        private CharacterController controller;
        private float verticalVelocity;

        private void Awake()
        {
            controller = GetComponent<CharacterController>();
            if (cameraTransform == null && Camera.main != null)
                cameraTransform = Camera.main.transform;
        }

        private void Update()
        {
            Vector2 input = Vector2.ClampMagnitude(MobileInputState.Movement, 1f);
            Vector3 forward = cameraTransform != null
                ? Vector3.ProjectOnPlane(cameraTransform.forward, Vector3.up).normalized
                : transform.forward;
            Vector3 right = cameraTransform != null
                ? Vector3.ProjectOnPlane(cameraTransform.right, Vector3.up).normalized
                : transform.right;

            Vector3 move = (forward * input.y + right * input.x) * moveSpeed;

            if (controller.isGrounded && verticalVelocity < 0f)
                verticalVelocity = -2f;

            if (controller.isGrounded && MobileInputState.JumpPressed)
                verticalVelocity = Mathf.Sqrt(jumpHeight * -2f * gravity);

            verticalVelocity += gravity * Time.deltaTime;
            move.y = verticalVelocity;

            controller.Move(move * Time.deltaTime);
        }
    }
}
''',
"Player/PlayerLookController.cs": r'''
using UnityEngine;
using PixelStrike.Mobile;

namespace PixelStrike.Player
{
    public sealed class PlayerLookController : MonoBehaviour
    {
        [SerializeField] private Transform playerBody;
        [SerializeField] private float sensitivity = 0.12f;
        [SerializeField] private float minPitch = -80f;
        [SerializeField] private float maxPitch = 80f;

        private float pitch;

        private void Update()
        {
            Vector2 look = MobileInputState.Look;
            if (look.sqrMagnitude < 0.0001f)
                return;

            pitch = Mathf.Clamp(pitch - look.y * sensitivity, minPitch, maxPitch);
            transform.localRotation = Quaternion.Euler(pitch, 0f, 0f);

            if (playerBody != null)
                playerBody.Rotate(Vector3.up, look.x * sensitivity);
        }
    }
}
''',
"Player/PlayerSpawnPoint.cs": r'''
using UnityEngine;

namespace PixelStrike.Player
{
    public sealed class PlayerSpawnPoint : MonoBehaviour
    {
        [SerializeField] private bool drawGizmo = true;

        public Vector3 Position => transform.position;
        public Quaternion Rotation => transform.rotation;

        private void OnDrawGizmos()
        {
            if (!drawGizmo) return;
            Gizmos.color = Color.cyan;
            Gizmos.DrawWireSphere(transform.position, 0.35f);
            Gizmos.DrawRay(transform.position, transform.forward * 1.5f);
        }
    }
}
''',
"Weapons/WeaponDefinition.cs": r'''
using UnityEngine;

namespace PixelStrike.Weapons
{
    [CreateAssetMenu(fileName = "WeaponDefinition", menuName = "PIXEL STRIKE/Weapon")]
    public sealed class WeaponDefinition : ScriptableObject
    {
        public string weaponName = "AKR";
        [Min(1)] public int damage = 25;
        [Min(1)] public int magazineSize = 30;
        [Min(0.05f)] public float shotsPerSecond = 10f;
        [Min(1f)] public float range = 100f;
        [Min(0f)] public float reloadSeconds = 2f;
        [Min(0f)] public float recoil = 1f;
        public bool automatic = true;
    }
}
''',
"Weapons/WeaponInventory.cs": r'''
using UnityEngine;

namespace PixelStrike.Weapons
{
    public sealed class WeaponInventory : MonoBehaviour
    {
        [SerializeField] private WeaponController[] weapons;
        private int activeIndex;

        public WeaponController ActiveWeapon =>
            weapons != null && weapons.Length > 0 &&
            activeIndex >= 0 && activeIndex < weapons.Length
                ? weapons[activeIndex] : null;

        public void SelectWeapon(int index)
        {
            if (weapons == null || index < 0 || index >= weapons.Length)
                return;

            activeIndex = index;

            for (int i = 0; i < weapons.Length; i++)
            {
                if (weapons[i] != null)
                    weapons[i].gameObject.SetActive(i == activeIndex);
            }
        }

        public void SelectNext()
        {
            if (weapons == null || weapons.Length == 0) return;
            SelectWeapon((activeIndex + 1) % weapons.Length);
        }
    }
}
''',
"Weapons/WeaponRecoilController.cs": r'''
using UnityEngine;

namespace PixelStrike.Weapons
{
    public sealed class WeaponRecoilController : MonoBehaviour
    {
        [SerializeField] private WeaponController weapon;
        [SerializeField] private Transform cameraPivot;
        [SerializeField] private float returnSpeed = 8f;
        [SerializeField] private float recoilMultiplier = 1f;

        private float currentRecoil;
        private float targetRecoil;

        private void OnEnable()
        {
            if (weapon != null)
                weapon.ShotFired += OnShotFired;
        }

        private void OnDisable()
        {
            if (weapon != null)
                weapon.ShotFired -= OnShotFired;
        }

        private void Update()
        {
            if (cameraPivot == null) return;

            targetRecoil = Mathf.Lerp(targetRecoil, 0f, returnSpeed * Time.deltaTime);
            currentRecoil = Mathf.Lerp(currentRecoil, targetRecoil, returnSpeed * Time.deltaTime);
            cameraPivot.localRotation *= Quaternion.Euler(-currentRecoil, 0f, 0f);
        }

        private void OnShotFired(Vector3 direction, float amount)
        {
            targetRecoil += amount * recoilMultiplier;
            targetRecoil = Mathf.Clamp(targetRecoil, 0f, 15f);
        }
    }
}
''',
"Combat/TeamMember.cs": r'''
using UnityEngine;

namespace PixelStrike.Combat
{
    public enum TeamId { Neutral, Alpha, Bravo }

    public sealed class TeamMember : MonoBehaviour
    {
        [SerializeField] private TeamId team = TeamId.Neutral;
        public TeamId Team => team;

        public bool IsEnemyOf(TeamMember other)
        {
            return other != null && team != TeamId.Neutral &&
                   other.team != TeamId.Neutral && team != other.team;
        }
    }
}
''',
"Combat/HitMarker.cs": r'''
using UnityEngine;

namespace PixelStrike.Combat
{
    public sealed class HitMarker : MonoBehaviour
    {
        [SerializeField] private GameObject markerVisual;
        [SerializeField] private float visibleSeconds = 0.12f;
        private float hideAt;

        public void Show()
        {
            if (markerVisual != null)
                markerVisual.SetActive(true);

            hideAt = Time.unscaledTime + visibleSeconds;
        }

        private void Update()
        {
            if (markerVisual != null && markerVisual.activeSelf &&
                Time.unscaledTime >= hideAt)
                markerVisual.SetActive(false);
        }
    }
}
''',
"AI/EnemyPatrol.cs": r'''
using UnityEngine;

namespace PixelStrike.AI
{
    public sealed class EnemyPatrol : MonoBehaviour
    {
        [SerializeField] private Transform[] points;
        [SerializeField] private float speed = 2f;
        [SerializeField] private float reachDistance = 0.2f;
        private int currentPoint;

        private void Update()
        {
            if (points == null || points.Length == 0 ||
                points[currentPoint] == null)
                return;

            Transform target = points[currentPoint];
            transform.position = Vector3.MoveTowards(
                transform.position, target.position, speed * Time.deltaTime);

            Vector3 direction = target.position - transform.position;
            direction.y = 0f;

            if (direction.sqrMagnitude > 0.01f)
                transform.rotation = Quaternion.Slerp(
                    transform.rotation,
                    Quaternion.LookRotation(direction),
                    5f * Time.deltaTime);

            if (Vector3.Distance(transform.position, target.position) <= reachDistance)
                currentPoint = (currentPoint + 1) % points.Length;
        }
    }
}
''',
"AI/EnemyTarget.cs": r'''
using UnityEngine;

namespace PixelStrike.AI
{
    public sealed class EnemyTarget : MonoBehaviour
    {
        [SerializeField] private Transform target;
        [SerializeField] private float detectionRange = 20f;
        [SerializeField] private float turnSpeed = 4f;

        public Transform Target => target;
        public bool HasTarget =>
            target != null &&
            Vector3.Distance(transform.position, target.position) <= detectionRange;

        public void SetTarget(Transform newTarget) => target = newTarget;

        private void Update()
        {
            if (!HasTarget) return;

            Vector3 direction = target.position - transform.position;
            direction.y = 0f;
            if (direction.sqrMagnitude < 0.001f) return;

            Quaternion look = Quaternion.LookRotation(direction);
            transform.rotation = Quaternion.Slerp(
                transform.rotation, look, turnSpeed * Time.deltaTime);
        }
    }
}
''',
"GameModes/MatchTimer.cs": r'''
using System;
using UnityEngine;

namespace PixelStrike.GameModes
{
    public sealed class MatchTimer : MonoBehaviour
    {
        [SerializeField, Min(1f)] private float durationSeconds = 300f;
        public float RemainingSeconds { get; private set; }
        public bool IsRunning { get; private set; }
        public event Action TimeExpired;

        private void Start()
        {
            ResetTimer();
            StartTimer();
        }

        private void Update()
        {
            if (!IsRunning) return;

            RemainingSeconds = Mathf.Max(0f, RemainingSeconds - Time.deltaTime);

            if (RemainingSeconds <= 0f)
            {
                IsRunning = false;
                TimeExpired?.Invoke();
            }
        }

        public void ResetTimer()
        {
            RemainingSeconds = durationSeconds;
            IsRunning = false;
        }

        public void StartTimer() => IsRunning = RemainingSeconds > 0f;
        public void PauseTimer() => IsRunning = false;
    }
}
''',
"GameModes/TeamDeathmatchRules.cs": r'''
using UnityEngine;

namespace PixelStrike.GameModes
{
    public sealed class TeamDeathmatchRules : MonoBehaviour
    {
        [SerializeField, Min(1)] private int scoreLimit = 50;
        public int AlphaScore { get; private set; }
        public int BravoScore { get; private set; }
        public bool MatchEnded { get; private set; }

        public void RegisterElimination(Combat.TeamId scoringTeam)
        {
            if (MatchEnded) return;

            if (scoringTeam == Combat.TeamId.Alpha) AlphaScore++;
            if (scoringTeam == Combat.TeamId.Bravo) BravoScore++;

            if (AlphaScore >= scoreLimit || BravoScore >= scoreLimit)
                MatchEnded = true;
        }

        public void ResetMatch()
        {
            AlphaScore = 0;
            BravoScore = 0;
            MatchEnded = false;
        }
    }
}
''',
"UI/AmmoHUD.cs": r'''
using UnityEngine;
using UnityEngine.UI;
using PixelStrike.Weapons;

namespace PixelStrike.UI
{
    public sealed class AmmoHUD : MonoBehaviour
    {
        [SerializeField] private WeaponController weapon;
        [SerializeField] private Text ammoText;

        private void OnEnable()
        {
            if (weapon != null) weapon.AmmoChanged += UpdateAmmo;
        }

        private void OnDisable()
        {
            if (weapon != null) weapon.AmmoChanged -= UpdateAmmo;
        }

        private void Start()
        {
            if (weapon != null)
                UpdateAmmo(weapon.AmmoInMagazine, weapon.MagazineSize);
        }

        private void UpdateAmmo(int current, int capacity)
        {
            if (ammoText != null)
                ammoText.text = current + " / " + capacity;
        }
    }
}
''',
"UI/HealthHUD.cs": r'''
using UnityEngine;
using UnityEngine.UI;
using PixelStrike.Combat;

namespace PixelStrike.UI
{
    public sealed class HealthHUD : MonoBehaviour
    {
        [SerializeField] private HealthController health;
        [SerializeField] private Slider healthBar;
        [SerializeField] private Text healthText;

        private void OnEnable()
        {
            if (health != null) health.HealthChanged += UpdateHealth;
        }

        private void OnDisable()
        {
            if (health != null) health.HealthChanged -= UpdateHealth;
        }

        private void Start()
        {
            if (health != null)
                UpdateHealth(health.CurrentHealth, health.MaxHealth);
        }

        private void UpdateHealth(int current, int maximum)
        {
            if (healthBar != null)
                healthBar.value = maximum > 0 ? (float)current / maximum : 0f;

            if (healthText != null)
                healthText.text = current + " HP";
        }
    }
}
''',
"UI/MatchHUD.cs": r'''
using UnityEngine;
using UnityEngine.UI;
using PixelStrike.GameModes;

namespace PixelStrike.UI
{
    public sealed class MatchHUD : MonoBehaviour
    {
        [SerializeField] private MatchTimer timer;
        [SerializeField] private TeamDeathmatchRules rules;
        [SerializeField] private Text timerText;
        [SerializeField] private Text scoreText;

        private void Update()
        {
            if (timer != null && timerText != null)
            {
                int seconds = Mathf.CeilToInt(timer.RemainingSeconds);
                timerText.text = (seconds / 60).ToString("00") + ":" +
                                 (seconds % 60).ToString("00");
            }

            if (rules != null && scoreText != null)
                scoreText.text = rules.AlphaScore + " : " + rules.BravoScore;
        }
    }
}
''',
"Settings/GraphicsSettingsController.cs": r'''
using UnityEngine;

namespace PixelStrike.Settings
{
    public sealed class GraphicsSettingsController : MonoBehaviour
    {
        private const string QualityKey = "PS_Quality";

        private void Start()
        {
            int saved = PlayerPrefs.GetInt(QualityKey, 1);
            ApplyQuality(saved);
        }

        public void ApplyQuality(int index)
        {
            if (QualitySettings.names.Length == 0) return;

            index = Mathf.Clamp(index, 0, QualitySettings.names.Length - 1);
            QualitySettings.SetQualityLevel(index, true);
            PlayerPrefs.SetInt(QualityKey, index);
            PlayerPrefs.Save();
        }

        public void SetLow() => ApplyQuality(0);
        public void SetMedium() => ApplyQuality(
            Mathf.Min(1, QualitySettings.names.Length - 1));
        public void SetHigh() => ApplyQuality(
            Mathf.Max(0, QualitySettings.names.Length - 1));
    }
}
''',
"Audio/AudioManager.cs": r'''
using UnityEngine;

namespace PixelStrike.Audio
{
    public sealed class AudioManager : MonoBehaviour
    {
        public static AudioManager Instance { get; private set; }

        [SerializeField] private AudioSource musicSource;
        [SerializeField] private AudioSource effectsSource;

        private const string MusicKey = "PS_Music";
        private const string EffectsKey = "PS_Effects";

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ApplyVolumes();
        }

        public void PlayEffect(AudioClip clip)
        {
            if (clip != null && effectsSource != null)
                effectsSource.PlayOneShot(clip);
        }

        public void SetMusicVolume(float value)
        {
            PlayerPrefs.SetFloat(MusicKey, Mathf.Clamp01(value));
            ApplyVolumes();
        }

        public void SetEffectsVolume(float value)
        {
            PlayerPrefs.SetFloat(EffectsKey, Mathf.Clamp01(value));
            ApplyVolumes();
        }

        private void ApplyVolumes()
        {
            if (musicSource != null)
                musicSource.volume = PlayerPrefs.GetFloat(MusicKey, 0.7f);

            if (effectsSource != null)
                effectsSource.volume = PlayerPrefs.GetFloat(EffectsKey, 0.8f);
        }
    }
}
''',
"Performance/FrameRateController.cs": r'''
using UnityEngine;

namespace PixelStrike.Performance
{
    public sealed class FrameRateController : MonoBehaviour
    {
        [SerializeField] private int targetFrameRate = 60;

        private void Awake()
        {
            Application.targetFrameRate = Mathf.Clamp(targetFrameRate, 30, 120);
            QualitySettings.vSyncCount = 0;
        }

        public void SetTargetFrameRate(int fps)
        {
            targetFrameRate = Mathf.Clamp(fps, 30, 120);
            Application.targetFrameRate = targetFrameRate;
        }
    }
}
'''
}

created = []
skipped = []

for relative_path, content in files.items():
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        skipped.append(str(path))
        continue

    path.write_text(content.strip() + "\n", encoding="utf-8")
    created.append(str(path))

print(f"Создано файлов: {len(created)}")
for item in created:
    print(" +", item)

if skipped:
    print(f"\nПропущено существующих файлов: {len(skipped)}")
    for item in skipped:
        print(" =", item)

print("\nГотово. Существующие файлы не перезаписывались.")
