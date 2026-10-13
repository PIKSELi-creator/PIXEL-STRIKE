
using System;
using System.Collections;
using UnityEngine;

namespace PixelStrike.Weapons
{
    public class WeaponController : MonoBehaviour
    {
        [Header("Основные характеристики")]
        [SerializeField] private string weaponName = "AKR";
        [SerializeField, Min(1)] private int damage = 25;
        [SerializeField, Min(1f)] private float fireRate = 10f;
        [SerializeField, Min(1f)] private float range = 100f;

        [Header("Боезапас")]
        [SerializeField, Min(1)] private int magazineSize = 30;
        [SerializeField, Min(0f)] private float reloadDuration = 2f;

        [Header("Отдача")]
        [SerializeField, Min(0f)] private float recoilAmount = 1f;

        [Header("Стрельба")]
        [SerializeField] private Camera playerCamera;
        [SerializeField] private LayerMask hitMask = ~0;

        public string Name => weaponName;
        public int Damage => damage;
        public int AmmoInMagazine { get; private set; }
        public int MagazineSize => magazineSize;
        public bool IsReloading { get; private set; }

        public event Action<int, int> AmmoChanged;
        public event Action<Vector3, float> ShotFired;

        private float nextFireTime;
        private Coroutine reloadRoutine;

        private void Awake()
        {
            AmmoInMagazine = magazineSize;

            if (playerCamera == null)
                playerCamera = Camera.main;

            NotifyAmmoChanged();
        }

        public bool TryFire()
        {
            if (IsReloading || Time.time < nextFireTime)
                return false;

            if (AmmoInMagazine <= 0)
            {
                StartReload();
                return false;
            }

            if (playerCamera == null)
            {
                Debug.LogWarning(
                    "PIXEL STRIKE: для оружия не назначена камера игрока."
                );
                return false;
            }

            nextFireTime = Time.time + 1f / fireRate;
            AmmoInMagazine--;
            NotifyAmmoChanged();

            Vector3 origin = playerCamera.transform.position;
            Vector3 direction = playerCamera.transform.forward;

            if (Physics.Raycast(
                origin,
                direction,
                out RaycastHit hit,
                range,
                hitMask,
                QueryTriggerInteraction.Ignore))
            {
                IDamageable target = hit.collider.GetComponentInParent<IDamageable>();

                if (target != null)
                    target.TakeDamage(damage);

                Debug.DrawLine(origin, hit.point, Color.red, 1f);
            }
            else
            {
                Debug.DrawRay(origin, direction * range, Color.yellow, 1f);
            }

            ShotFired?.Invoke(direction, recoilAmount);
            return true;
        }

        public void StartReload()
        {
            if (IsReloading || AmmoInMagazine >= magazineSize)
                return;

            if (reloadRoutine != null)
                StopCoroutine(reloadRoutine);

            reloadRoutine = StartCoroutine(ReloadRoutine());
        }

        private IEnumerator ReloadRoutine()
        {
            IsReloading = true;
            yield return new WaitForSeconds(reloadDuration);

            AmmoInMagazine = magazineSize;
            IsReloading = false;
            reloadRoutine = null;

            NotifyAmmoChanged();
        }

        private void NotifyAmmoChanged()
        {
            AmmoChanged?.Invoke(AmmoInMagazine, magazineSize);
        }
    }
}

