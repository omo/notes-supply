
import time
from absl import flags # type: ignore
from absl import app

from icws import launch_fresh
from launcher import Perfetto
import icws

FLAGS = flags.FLAGS

flags.DEFINE_string('activity',
                    'com.twitter.android/.StartActivity',
#                   'com.instagram.android/.activity.MainTabActivity',
                    'The activity to launch')

flags.DEFINE_string('trace',
                    'twitter-scroll.pftracce.gz',
#                   'instagram-scroll.pftracce.gz',
                    'The trace file name')

def main(argv):
    launch_fresh(FLAGS.activity)
    time.sleep(1)

    with Perfetto(FLAGS.trace):
        for _ in range(5):
            icws.ashell('input touchscreen swipe 540 1160 540 580 20')
            time.sleep(1)

if __name__ == '__main__':
  app.run(main)