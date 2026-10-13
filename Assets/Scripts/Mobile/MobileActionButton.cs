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
