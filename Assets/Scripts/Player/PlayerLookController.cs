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
