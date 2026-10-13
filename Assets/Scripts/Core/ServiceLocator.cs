using System;
using System.Collections.Generic;

public static class ServiceLocator
{
    private static readonly Dictionary<Type, object> Services = new();

    public static void Register<T>(T service) where T : class
    {
        if (service == null)
            throw new ArgumentNullException(nameof(service));

        Services[typeof(T)] = service;
    }

    public static bool TryGet<T>(out T service) where T : class
    {
        if (Services.TryGetValue(typeof(T), out object value))
        {
            service = value as T;
            return service != null;
        }

        service = null;
        return false;
    }

    public static T Get<T>() where T : class
    {
        if (TryGet<T>(out T service))
            return service;

        throw new InvalidOperationException(
            $"Service {typeof(T).Name} has not been registered.");
    }

    public static void Unregister<T>() where T : class
    {
        Services.Remove(typeof(T));
    }

    public static void Clear()
    {
        Services.Clear();
    }
}
