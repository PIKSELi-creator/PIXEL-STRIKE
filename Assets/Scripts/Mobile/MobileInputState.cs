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
