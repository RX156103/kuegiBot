from kuegi_bot.backtest_engine import BackTest
from kuegi_bot.utils.helper import load_bars, prepare_plot
from kuegi_bot.utils import log
from kuegi_bot.kuegi_channel import KuegiChannel
from kuegi_bot.bots.kuegi_bot import KuegiBot
from kuegi_bot.bots.sfp_bot import SfpBot

logger = log.setup_custom_logger()

def plot(bars):
    forplot= bars[:]

    logger.info("initializing indicators")
    indis = [KuegiChannel()]

    logger.info("preparing plot")
    fig= prepare_plot(forplot, indis)
    fig.show()

def backtest(bars):
    bots= [KuegiBot(max_look_back=13, threshold_factor=3, buffer_factor=0.1,
                  max_dist_factor=1, max_swing_length=2,
                  max_channel_size_factor=6, risk_factor=1000, entry_tightening=1,
                  stop_entry=False, trail_to_swing=True, delayed_entry=True),
           KuegiBot(max_look_back=13, threshold_factor=3, buffer_factor=0.1,
                    max_dist_factor=1, max_swing_length=2,
                    max_channel_size_factor=6, risk_factor=1000, entry_tightening=1,
                    stop_entry=True, trail_to_swing=True, delayed_entry=True)]
    for bot in bots:
        BackTest(bot,bars).run()

def runOpti(bars):
    for mask in range(0x1F):
        params= []
        for i in range(5):
            params.append((mask & (1 << i)) != 0)
        logger.info(str(mask))
        bot=KuegiBot(logger=logger,
            max_look_back=13, threshold_factor=0.9, buffer_factor=0.05,
            max_dist_factor=2, max_swing_length=3,
            max_channel_size_factor=6, risk_factor=0.1, entry_tightening=1, bars_till_cancel_triggered=5,
            be_factor=2, allow_trail_back=params[0],
            stop_entry=params[1], trail_to_swing=params[2], delayed_entry=params[3], delayed_cancel=params[4]
        )
        BackTest(bot, bars).run()


bars_b = load_bars(30 * 12, 240,0,'bybit')
#bars_m = load_bars(30 * 24, 240,0,'bitmex')
#backtest(bars)

#bars1= load_bars(24)
#bars2= process_low_tf_bars(m1_bars, 240, 60)
#bars3= process_low_tf_bars(m1_bars, 240, 120)
#bars4= process_low_tf_bars(m1_bars, 240, 180)


'''

##### SFP 240

bot = SfpBot(logger=logger, directionFilter=0, risk_factor=1,
             max_look_back=21, threshold_factor=0.8, buffer_factor=0.05, max_dist_factor=1, max_swing_length=4,
             be_factor=1, min_wick_fac=0.1, min_swing_length=2,
             init_stop_type=1, tp_fac=20
             )

BackTest(bot, bars_b).run()

bot.create_performance_plot().show()


bot = SfpBot(logger=logger, directionFilter=0, risk_factor=1,
             max_look_back=21, threshold_factor=0.8, buffer_factor=0.05, max_dist_factor=1, max_swing_length=4,
             be_factor=1, min_wick_fac=0.3, min_swing_length=2,
             init_stop_type=0, tp_fac=25
             )

BackTest(bot, bars_m).run()

bot.create_performance_plot().show()



bybit 12: pos: 224 | profit: 21.66 | HH: 25.84 | maxDD: 22.96 | rel: 0.94 | UW days: 124.9

             max_look_back=21, threshold_factor=0.8, buffer_factor=0.05, max_dist_factor=1, max_swing_length=4,
             be_factor=1, min_wick_fac=0.1, min_swing_length=2,
             init_stop_type=1, tp_fac=20
             


bitmex 24:  pos: 402 | profit: 74.82 | HH: 85.44 | maxDD: 29.01 | rel: 2.58 | UW days: 250.1

             max_look_back=21, threshold_factor=0.8, buffer_factor=0.05, max_dist_factor=1, max_swing_length=4,
             be_factor=1, min_wick_fac=0.3, min_swing_length=2,
             init_stop_type=0, tp_fac=25


############## Kuegi Bot

bot=KuegiBot(logger=logger, directionFilter= 0,
    max_look_back=13, threshold_factor=2.5, buffer_factor=-0.0618,
    max_dist_factor=1, max_swing_length=4,
    min_channel_size_factor=1.618, max_channel_size_factor=16, 
    risk_factor=1, max_risk_mul=2, risk_type= 0,
    entry_tightening=0.1, bars_till_cancel_triggered=3,
    be_factor= 2, allow_trail_back= True,
    stop_entry=True, trail_to_swing=False, delayed_entry=False, delayed_cancel=True
)

BackTest(bot, bars_m).run()

bot.create_performance_plot().show()


bot=KuegiBot(logger=logger, directionFilter= 0,
    max_look_back=13, threshold_factor=0.8, buffer_factor=0.05,
    max_dist_factor=2, max_swing_length=4,
    min_channel_size_factor=0, max_channel_size_factor=16, 
    risk_factor=1, max_risk_mul=2, risk_type= 1,
    entry_tightening=1, bars_till_cancel_triggered=5,
    be_factor= 1.5, allow_trail_back= False,
    stop_entry=True, trail_to_swing=False, delayed_entry=True, delayed_cancel=True
)
BackTest(bot, bars_b).run()

bot.create_performance_plot().show()

#'''

#BackTest(bot, bars1).run().prepare_plot().show()

''' results on 24 month test    

12 mo bybit:  pos: 168 | profit: 43.14 | HH: 50.95 | maxDD: 12.41 | rel: 3.48 | UW days: 43.8
12 mo bitmex: pos: 180 | profit: 26.76 | HH: 26.76 | maxDD: 30.17 | rel: 0.89 | UW days: 199.9
24 mo bitmex: pos: 321 | profit: 4.78 | HH: 18.93 | maxDD: 42.59 | rel: 0.11 | UW days: 290.3
original: pos: 319 | profit: 39.17 | HH: 39.17 | maxDD: 30.71 | rel: 1.28 | UW days: 202.4
    max_look_back=13, threshold_factor=0.9, buffer_factor=0.05,
    max_dist_factor=2, max_swing_length=3,
    min_channel_size_factor=0, max_channel_size_factor=6, 
    risk_factor=1, entry_tightening=1, bars_till_cancel_triggered=5,
    be_factor= 1.5, allow_trail_back= False,
    stop_entry=True, trail_to_swing=True, delayed_entry=True, delayed_cancel=True
    
##########
Bybit Opti:
    
Fokus relation 
12 mo bybit: pos: 178 | profit: 97.55 | HH: 109.59 | maxDD: 13.52 | rel: 7.22 | UW days: 41.5
12 mo bitmex: pos: 185 | profit: 0.15 | HH: 10.47 | maxDD: 31.43 | rel: 0.00 | UW days: 207.2
    max_look_back=13, threshold_factor=0.8, buffer_factor=0.05,
    max_dist_factor=2, max_swing_length=4,
    min_channel_size_factor=0, max_channel_size_factor=16, 
    risk_factor=1, max_risk_mul=2, risk_type= 1,
    entry_tightening=1, bars_till_cancel_triggered=5,
    be_factor= 1.5, allow_trail_back= False,
    stop_entry=True, trail_to_swing=False, delayed_entry=True, delayed_cancel=True


#############
Bitmex Opti
Fokus on Profit/DD: 
12 mo bybit pos: 266 | profit: 50.77 | HH: 66.65 | maxDD: 22.89 | rel: 2.22 | UW days: 94.93

12 months: pos: 280 | profit: 109.04 | HH: 116.86 | maxDD: 16.86 | rel: 6.47 | UW days: 72.6
24 months: pos: 565 | profit: 157.49 | HH: 176.51 | maxDD: 19.68 | rel: 8.00 | UW days: 72.6
48 months: pos: 1145 | profit: 363.90 | HH: 371.72 | maxDD: 22.25 | rel: 16.35 | UW days: 72.6
    max_look_back=13, threshold_factor=2.5, buffer_factor=-0.0618,
    max_dist_factor=1, max_swing_length=4,
    min_channel_size_factor=1.618, max_channel_size_factor=16, 
    risk_factor=1, max_risk_mul=3, risk_type= 0,
    entry_tightening=0.1, bars_till_cancel_triggered=3,
    be_factor= 2, allow_trail_back= True,
    stop_entry=True, trail_to_swing=False, delayed_entry=False, delayed_cancel=True


low UW: 
24 months: pos: 383 | profit: 91.10 | HH: 101.66 | maxDD: 13.25 | rel: 6.88 | UW days: 55.9
48 months: pos: 763 | profit: 224.53 | HH: 228.34 | maxDD: 16.29 | rel: 13.78 | UW days: 140.0
    max_look_back=13, threshold_factor=2.5, buffer_factor=-0.0618,
    max_dist_factor=1, max_swing_length=4,
    min_channel_size_factor=0, max_channel_size_factor=16.18, 
    risk_factor=1, max_risk_mul=2, risk_type= 2,
    entry_tightening=0,bars_till_cancel_triggered=3,
    be_factor= 2, allow_trail_back= True,
    stop_entry=True, trail_to_swing=False, delayed_entry=True, delayed_cancel=True



buffer 0: pos: 516 | profit: 120.09 | HH: 125.58 | maxDD: 24.49 | rel: 4.90 | UW days: 97.3
    max_look_back=13, threshold_factor=2.5, buffer_factor=0,
    max_dist_factor=1, max_swing_length=3,
    max_channel_size_factor=6, risk_factor=1, entry_tightening=0,bars_till_cancel_triggered=3,
    be_factor= 2, allow_trail_back= True,
    stop_entry=True, trail_to_swing=False, delayed_entry=False, delayed_cancel=True

'''