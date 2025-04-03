    s_values = np.logspace(np.log10(0.8), np.log10(1.2), 50)
    times, vs = [], []

    for s in tqdm(s_values):
        t, var = simulate_s(s)
        times.append(t); vs.append(var)

    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(s_values, vs, label='var')
    plt.xlabel('s'); plt.ylabel('var')
    plt.xlim(0.8, 1.2); plt.grid(True)
    plt.xticks(np.arange(0.8, 1.2, 0.05))

    plt.subplot(2, 1, 2)
    plt.plot(s_values, times, label='times')
    plt.xlabel('s'); plt.ylabel('times')
    plt.xlim(0.8, 1.2); plt.grid(True)
    plt.xticks(np.arange(0.8, 1.2, 0.05))

    plt.tight_layout()
    plt.show()