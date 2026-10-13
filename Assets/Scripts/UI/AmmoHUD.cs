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
