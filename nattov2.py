





    def check_netbeat():
        hb = True   
        while hb:
            try:
                hentai_sane = Hentai.exists(177013)
                print(f'Hentai Heartbeat : {hentai_sane}')
                return True
            except TypeError as e:
                print('Flat line : ',e)
                return False
            
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                
                f1 = executor.submit(check_netbeat)
                print(f1.result())
            