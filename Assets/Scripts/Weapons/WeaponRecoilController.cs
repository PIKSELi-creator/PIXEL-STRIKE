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
