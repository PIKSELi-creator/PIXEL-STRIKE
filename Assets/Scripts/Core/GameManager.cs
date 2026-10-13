using UnityEngine;

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    public GameState CurrentState { get; private set; } = GameState.Boot;

    public event System.Action<GameState> StateChanged;

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }

        Instance = this;
        DontDestroyOnLoad(gameObject);
        Application.targetFrameRate = 60;
        Screen.sleepTimeout = SleepTimeout.Never;
    }

    public bool SetState(GameState nextState)
    {
        if (CurrentState == nextState)
            return false;

        CurrentState = nextState;
        StateChanged?.Invoke(nextState);
        Debug.Log($"[PIXEL STRIKE] State: {nextState}");
        return true;
    }

    private void OnDestroy()
    {
        if (Instance == this)
            Instance = null;
    }
}
