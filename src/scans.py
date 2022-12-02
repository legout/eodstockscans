def EOD(scale={"volume": 1, "price": 1}):
    min_volume = f"volume>{200000*scale['volume']}"
    min_average_volume = f"sma(50,volume)>{200000*scale['volume']}"
    min_dollar_volume = f"volume*close>{2000000*scale['volume']*scale['price']}"
    min_average_dollar_volume = (
        f"sma(50,volume)*sma(50)>{2000000*scale['volume']*scale['price']}"
    )
    min_price = f"close>{4*scale['price']}"

    eod = {
        "Kristjan Kullamägi": {
            "link": "https://twitter.com/Qullamaggie",
            "scans": {
                "Biggest Gainers 1M": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND adr(20)>4 AND ti>0.9",
                    "order": "close/min(21)",
                    "limit": 200,
                },
                "Biggest Gainers 3M": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND adr(20)>4 AND ti>0.9",
                    "order": "close/min(63)",
                    "limit": 200,
                },
                "Biggest Gainers 6M": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND adr(20)>4 AND ti>0.9",
                    "order": "close/min(126)",
                    "limit": 200,
                },
                "Biggest Gainers 12M": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND adr(20)>4 AND ti>0.9",
                    "order": "close/min(252)",
                    "limit": 200,
                },
                "EP with Growth": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND sma(20)>sma(50) AND close>sma(50) AND open/close(1)>1.03 AND market_cap>500000000 AND market_cap<100000000000 AND revenue_growth>0.3 AND earnings_estimate_p1y_growth>0.15",
                    "order": "volume/sma(50,volume)",
                    "limit": 100,
                },
                "EP": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND sma(20)>sma(50) AND close>sma(50) AND open/close(1)>1.03 AND market_cap>500000000 AND market_cap<100000000000",
                    "order": "volume/sma(50,volume)",
                    "limit": 100,
                },
                "High Trend Intensity": {
                    "query": f"{min_price} AND close<20 AND {min_average_volume} AND {min_dollar_volume} AND ti>1.08 AND adr(20)>4",
                    "order": "close/min(126)",
                    "limit": 200,
                },
                "Small Stock Momo": {
                    "query": "close/close(1)>1.1 AND close<10 AND sma(50,volume)>200000",
                    "order": "roc",
                    "limit": 200,
                },
                "Momentum": {
                    "query": f"close>high(1) AND adr(1)/adr(20)>1 AND {min_average_volume} AND {min_dollar_volume}",
                    "order": "roc",
                    "limit": 200,
                },
            },
        },
        "Brad Schulz": {
            "link": "https://twitter.com/BSchulz33868165",
            "scans": {
                "Pocket Pivot": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND volume>ema(50,volume) AND close/close(1)>=1.05 AND close>ema(200) AND high-close<0.5*close-0.5*low AND pp",
                    "order": "volume/sma(50,volume)",
                    "limit": 100,
                }
            },
        },
        "Stockbee": {
            "link": "https://twitter.com/PradeepBonde",
            "scans": {
                "4 PCT  Gainers": {
                    "query": f"{min_price} AND close/close(1)>1.04 AND close(1)-open(1)<close-open AND close(1)/close(2)<=1.02 AND {min_average_volume} AND volume>volume(1) AND close-low>0.7*high-0.7*low",
                    "order": "roc",
                    "limit": 100,
                },
                "Combo": {
                    "query": f"close-open>0.9 AND volume>200000 AND close(1)-open(1)<close-open AND close(1)/close(2)<1.02 AND close-low>0.7*high-0.7*low AND close>3 OR {min_price} AND close/close(1)>1.04 AND close(1)/close(2)<=1.02 AND volume>200000 AND volume>volume(1) AND close-low>0.7*high-0.7*low AND close>3",
                    "order": "roc",
                    "limit": 100,
                },
                "Ants": {
                    "query": f"{min_price} AND min(3,volume)>100000 AND ti>1.04 AND close/close(1)>=-1.01 AND close/close(1)<=1.01",
                    "order": "roc",
                    "limit": 100,
                },
                "Breakout 1M Base": {
                    "query": "close(1)/min(21)<=1.1 AND close/max(21)>=0.9 AND close/close(1)>=1.04 AND volume>200000 AND volume/volume(1) AND sma(50,volume)*close>2000000 AND close-low>0.7*high-0.7*low",
                    "order": "close/min(63)",
                    "limit": 100,
                },
                "Breakout 3M Base": {
                    "query": "close(1)/min(63)<=1.1 AND close/max(63)>=0.9 AND close/close(1)>=1.04 AND volume>200000 AND volume/volume(1) AND sma(50,volume)*close>2000000 AND close-low>0.7*high-0.7*low",
                    "order": "close/min(126)",
                    "limit": 100,
                },
            },
        },
        "Leif Soreide": {
            "link": "https://twitter.com/LeifSoreide",
            "scans": {
                "HTF": {
                    "query": f"{min_price} AND sma(20,volume)>250000 AND slope(10,sma(50,volume))<0 AND close>sma(50) AND sma(50)>sma(200) AND slope(10,sma(200))>0 AND close/min(40)>1.9 AND roc(60)>50 AND natr(14)<8 AND slope(10,natr(14))<0",
                    "order": "sctr",
                    "limit": 100,
                }
            },
        },
        "Blake Davis": {
            "link": "https://twitter.com/blakedavis50",
            "scans": {
                "Strength": {
                    "query": f"close>7*{scale['price']} AND {min_average_volume} AND {min_dollar_volume} AND ibd_rs_rank>70 AND ibd_industry_rs_rank>50 AND close-low>0.7*high-0.7*low AND close/close(1)>1",
                    "order": "ibd_rs_3m",
                    "limit": 200,
                }
            },
        },
        "Ben": {
            "link": "https://twitter.com/PatternProfits",
            "scans": {
                "Power of 3": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND close/ema(10)>0.985 AND close/ema(10)<1.01 AND close/ema(21)>0.985 AND close/ema(21)<1.01 AND close/sma(50)>0.985 AND close/sma(50)<1.01 AND ibd_rs_rank>=70",
                    "order": "ibd_rs",
                    "limit": 100,
                },
                "Velocity": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND close/close(1)>1.03 AND volume/sma(50,volume)>1.3 AND ibd_rs_rank>70 AND float_shares<100000000 AND ti>1.05",
                    "order": "ibd_rs_3m",
                    "limit": 100,
                },
                "Focus": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND ibd_industry_rs_rank>70 AND ibd_rs_3m_rank>70 AND earnings_estimate_p1y_growth>=0.25 AND revenue_growth>0.3",
                    "order": "ibd_rs_3m",
                    "limit": 100,
                },
            },
        },
        "Ray": {
            "link": "https://twitter.com/RayTL_",
            "scans": {
                "RSNHBP 5D": {
                    "query": f"rs=max(5,rs) AND close<max(5) AND {min_average_volume} AND {min_dollar_volume}",
                    "order": "close/min(5)",
                    "limit": 200,
                },
                "RSNHBP 1M": {
                    "query": f"rs=max(21,rs) AND close<max(21) AND {min_average_volume} AND {min_dollar_volume}",
                    "order": "close/min(21)",
                    "limit": 200,
                },
                "RSNHBP 3M": {
                    "query": f"rs=max(63,rs) AND close<max(63) AND {min_average_volume} AND {min_dollar_volume}",
                    "order": "close/min(63)",
                    "limit": 200,
                },
                "RSNHBP 6M": {
                    "query": f"rs=max(126,rs) AND close<max(126) AND {min_average_volume} AND {min_dollar_volume}",
                    "order": "close/min(126)",
                    "limit": 200,
                },
                "RSNHBP 12M": {
                    "query": f"rs=max(252,rs) AND close<max(252) AND {min_average_volume} AND {min_dollar_volume}",
                    "order": "close/min(252)",
                    "limit": 200,
                },
            },
        },
        "Mark Minvervini": {
            "link": "https://twitter.com/markminervini",
            "scans": {
                "Trend Template": {
                    "query": "close>sma(50) AND sma(50)>sma(150) AND sma(150)>sma(200) AND sma(200,close(22))<sma(200) AND close/min(252)>=1.30 AND close/max(252)>=0.75 AND ibd_rs_rank>70",
                    "order": "ibd_rs",
                    "limit": 200,
                }
            },
        },
        "Vo": {
            "link": "https://twitter.com/LignoL23",
            "scans": {
                "Top Gainers From Open": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND close/open>1.04",
                    "order": "close/open",
                    "limit": 100,
                },
                "Top Gainers": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND roc>4",
                    "order": "roc",
                    "limit": 100,
                },
                "Volume Gainers": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND roc>0",
                    "order": "volume/sma(50,volume)",
                    "limit": 200,
                },
                "Insiders": {
                    "query": f"{min_price} AND close<20 AND {min_average_volume} AND {min_dollar_volume} AND held_percent_insiders>0.5 AND float_shares<100000000",
                    "order": "close/min(252)",
                    "limit": 100,
                },
                "Darvas Scan": {
                    "query": f"{min_price} AND close/max(252)>0.85 AND close/min(252)>=1.7 AND ibd_sect_rs_3m_rank>75 AND {min_average_volume} AND {min_dollar_volume} AND volume/sma(50,volume)",
                    "order": "close/min(252)",
                    "limit": 100,
                },
                "Darvas Scan with Growth": {
                    "query": f"{min_price} AND close/max(252)>0.85 AND close/min(252)>=1.7 AND ibd_sect_rs_3m_rank>75 AND {min_average_volume} AND {min_dollar_volume} AND volume/sma(50,volume) AND revenue_growth>0.3 AND earnings_estimate_p1y_growth>0.15",
                    "order": "close/min(252)",
                    "limit": 100,
                },
                "52W High": {
                    "query": f"{min_price} AND {min_average_volume} AND {min_dollar_volume} AND close=max(252,close) AND volume/sma(50,volume)>1",
                    "order": "volume/sma(50,volume)",
                    "limit": 200,
                },
                "Quite and Tight": {
                    "query": f"{min_price} AND {min_average_volume} AND adr(20)>5 AND slope(10,adr(20))<0 AND ti>1 AND close/min(63)>1.75 AND cw(3,close)<3 AND volume/sma(50,volume)<0.75 AND sma(5,volume)<sma(50,volume)",
                    "order": "close/min(63)",
                    "limit": 200,
                },
                "Mo Scan": {
                    "query": f"{min_average_volume} AND market_cap>300000000 AND sma(20)>sma(20,close(1)) AND sma(50)>sma(50,close(1)) AND sma(20)>sma(50) AND sma(50)>sma(200) AND slope(2,atr(14))<0 AND ti>1.05 AND adr(10)>1.9",
                    "order": "ibd_rs",
                    "limit": 200,
                },
            },
        },
    }

    return eod


def INTRAY(scale=1):
    intraday = {}
    return intraday

