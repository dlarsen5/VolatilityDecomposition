import DailyVolDecomposition
import logging
import time
import multiprocessing
import os

def check_if_data_exists(symbol):
    data_path = 'Volatility Data/%s' % symbol

    if os.path.exists(data_path):
        return True

    return False

def main():

    symbols = [x[:-4] for x in os.listdir('Minute Prices/')]

    while True:
        print('Stock Tickers:')
        print(', '.join(symbols))
        print('\n')
        print('Type a stock symbol to calculate or "all" for all or "quit" to exit\n')
        inp = input('Input: ')
        inp = inp.upper()

        if inp == 'ALL':
            print('Starting...')
            symbols_to_calc = []
            #check if symbol already calculated
            for sym in symbols:
                if not check_if_data_exists(sym):
                    symbols_to_calc.append(sym)
            if len(symbols_to_calc) > 0:
                with multiprocessing.Pool(processes=None) as pool:
                    list_of_returns = pool.map(DailyVolDecomposition.process, symbols)
            print('All Done')
            print('\n')
            break

        elif inp in symbols:
            print('Starting...')
            DailyVolDecomposition.process(inp)
            print('All Done')
            print('\n')
        elif inp == 'QUIT':
            print('Bye Bye')
            break
        else:
            print('Input error, please retry')
            print('\n')

if __name__ == '__main__':

    log_file = 'Logs/run.log'
    if os.path.exists(log_file):
        os.remove(log_file)

    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    logging.info('Starting at %s' % time.time())
    main()
    logging.info('Finished at %s' % time.time())

