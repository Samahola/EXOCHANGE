import ccxt
import time
import csv

# Skapa en instans av Binance-klienten
binance = ccxt.binance()

# Sätt symbolen och tidsintervallet (3 dagar)
symbol = 'BTC/USDT'
since = binance.milliseconds() - 3 * 24 * 60 * 60 * 1000  # senaste 3 dagarna

# Initiera räknevariabler för köp- och säljorder
buy_orders = 0
sell_orders = 0
buy_volume = 0
sell_volume = 0

# Öppna en fil för att spara resultaten
with open('historical_trades.csv', 'w', newline='') as csvfile:
    # Skapa en CSV-skrivare
    csvwriter = csv.writer(csvfile)
    
    # Skriv rubriker till CSV-filen
    csvwriter.writerow(['Timestamp', 'Side', 'Price', 'Amount'])

    # Hämta handelsdata för de senaste 3 dagarna
    while since < binance.milliseconds():
        trades = binance.fetch_trades(symbol, since=since, limit=1000)
        
        if len(trades) == 0:
            break  # Om inga fler trades finns, avbryt loopen
        
        for trade in trades:
            # Spara varje trade i CSV-filen
            csvwriter.writerow([trade['timestamp'], trade['side'], trade['price'], trade['amount']])
            
            # Uppdatera räknevariablerna
            if trade['side'] == 'buy':
                buy_orders += 1
                buy_volume += trade['amount']
            elif trade['side'] == 'sell':
                sell_orders += 1
                sell_volume += trade['amount']
        
        # Uppdatera 'since' till tiden för den senaste traden + 1 ms
        since = trades[-1]['timestamp'] + 1
        
        # Vänta en kort stund för att undvika att överskrida API-begränsningar
        time.sleep(1)

# Efter loopningen, skriv ut sammanfattningen
print(f"Antal köporders: {buy_orders}, Total köpt volym: {buy_volume}")
print(f"Antal säljorders: {sell_orders}, Total såld volym: {sell_volume}")

# Avgör om det har varit flest köp- eller säljorder
if buy_orders > sell_orders:
    print("Det har varit flest köporders de senaste 3 dygnen.")
elif sell_orders > buy_orders:
    print("Det har varit flest säljorders de senaste 3 dygnen.")
else:
    print("Antalet köp- och säljorders är lika de senaste 3 dygnen.")
