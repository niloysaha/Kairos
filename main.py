import sys
from tv import mail


def print_disclaimer():
    print("DISCLAIMER")
    print("You are permitted to load the Kairos software (for example a PC, laptop, mobile or tablet) under your control. You are responsible for ensuring your device meets the minimum requirements of the Kairos software.")
    print("You are not permitted to:")
    print("\t* Edit, alter, modify, adapt, translate or otherwise change the whole or any part of the Software nor permit the whole or any part of the Software to be combined with or become incorporated in any other software, nor decompile, disassemble or reverse engineer the Software or attempt "
          "to do any such things")
    print("\t* Reproduce, copy, distribute, resell or otherwise use the Software for any commercial purpose")
    print("\t* Allow any third party to use the Software on behalf of or for the benefit of any third party")
    print("\t* Use the Software in any way which breaches any applicable local, national or international law")
    print("\t* use the Software for any purpose that Sanne Appel considers is a breach of the EULA agreement")
    print("You should have received a copy of the EULA agreement along with this program (LICENSE.md), If not, see https://eulatemplate.com/live.php?token=F2am7Ud98HlFDECoTq2GYhIksQmn6T9A\n")


def print_help():
    print("HELP")
    print("usage: python main.py [<file>] [-s|-s <minutes>] [-h] [-d]\n")
    print("<file>\t\t YAML file with alert definitions and/or summary option")
    print("-s\t\t Flag. Read your mailbox, create summary and send it to your mailbox. See kairos.cfg.")
    print("<minutes>\t Delay creating a summary for <number> of minutes (e.g. to allow alerts to get triggered first).")
    print("-h\t\t Flag. Show this help.")
    print("-d\t\t Flag. Show disclaimer.\n")


def main():
    from tv import tv

    try:
        print_disclaimer()
        print("USAGE\npython main.py [<file>] [-s|-s <minutes>] [-h] [-d]")
        print("For help, type: python main.py -h\n")
        # test_mongodb()
        yaml = ""
        send_summary = False
        delay_summary = 0
        i = 1
        while i < len(sys.argv):
            if str(sys.argv[i]).endswith('.yaml'):
                yaml = sys.argv[i]
            elif str(sys.argv[i]) == '-s':
                send_summary = True
            elif str(sys.argv[i]) == '-h':
                print_help()
            elif str(sys.argv[i]) == '-d':
                print_disclaimer()
            elif i > 1 and str(sys.argv[(i-1)]) == '-s':
                delay_summary = int(sys.argv[i])
            elif not str(sys.argv[i]).endswith('main.py'):
                print("No such argument: " + str(sys.argv[i]))
            i += 1

        triggered_signals = []
        if len(yaml) > 0:
            send_signals_immediately = not send_summary
            triggered_signals = tv.run(yaml, send_signals_immediately)
        if send_summary:
            mail.run(delay_summary, yaml, triggered_signals)
    except Exception as e:
        print(e)
    finally:
        exit(0)


def test_mongodb():
    import os
    CURRENT_DIR = os.path.curdir

    from kairos import tools
    log = tools.log
    log.setLevel(20)
    config = tools.get_config(CURRENT_DIR)
    log.setLevel(config.getint('logging', 'level'))

    connection_string = config.get('mongodb', 'connection_string')
    collection = config.get('mongodb', 'collection')

    from kairos import mongodb
    mongodb.test(connection_string, collection)
    exit(0)


main()
