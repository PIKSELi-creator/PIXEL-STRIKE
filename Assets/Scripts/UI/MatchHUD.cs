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
