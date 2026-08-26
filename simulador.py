import heapq

semente = 42

def random():
    global semente
    a = 1664525
    c = 1013904223
    m = 2**32
    semente = (a * semente + c) % m
    return semente / m

def f(a, b, u):
    return a + (b - a) * u

def roda_simulacao(c, k, cheg_min, cheg_max, serv_min, serv_max):
    global semente
    semente = 42
    
    n = 0
    t = 0
    last_t = 0
    tempos = [0] * (k + 1)
    perdas = 0
    total_rands = 0
    
    eventos = []
    heapq.heappush(eventos, (3.0, 'chegada'))
    
    while eventos:
        t, tipo = heapq.heappop(eventos)
        
        tempos[n] += (t - last_t)
        last_t = t
        
        if tipo == 'chegada':
            u1 = random()
            total_rands += 1
            tec = f(cheg_min, cheg_max, u1)
            is_last = (total_rands >= 100000)
            
            if not is_last:
                heapq.heappush(eventos, (t + tec, 'chegada'))
            
            if n < k:
                n += 1
                if n <= c:
                    if is_last:
                        break
                    u2 = random()
                    total_rands += 1
                    ts = f(serv_min, serv_max, u2)
                    heapq.heappush(eventos, (t + ts, 'saida'))
                    if total_rands >= 100000:
                        break
            else:
                perdas += 1
                
            if is_last:
                break
                
        else: # saida
            esperando = (n > c)
            n -= 1
            if esperando:
                u = random()
                total_rands += 1
                ts = f(serv_min, serv_max, u)
                heapq.heappush(eventos, (t + ts, 'saida'))
                if total_rands >= 100000:
                    break
                    
    tempo_total = sum(tempos)
    print("--- simulacao ---")
    print("c =", c, "K =", k, f"chegadas({cheg_min}...{cheg_max}) servico({serv_min}...{serv_max})")
    print("tempo global:", t)
    print("perdas:", perdas)
    
    probs = [x / tempo_total for x in tempos]
    media = 0
    for i in range(k+1):
        media += i * probs[i]
        
    print("populacao media:", media)
    print("estados:")
    for i in range(k+1):
        print(f"  {i}: {tempos[i]:.2f} min ({probs[i]*100:.2f}%)")
    print()

roda_simulacao(1, 5, 2.0, 5.0, 3.0, 5.0)
roda_simulacao(2, 5, 2.0, 5.0, 3.0, 5.0)
