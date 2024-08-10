#!python3
""" 
BairesMesh grumpy chat BOT
"""
import sys
import logging
import time
import random
import traceback
from datetime import datetime

__description__ = "BairesMesh grumpy chat BOT"
__version__ = 1.0

try:
    import pyqrcode # type: ignore[import-untyped]
    from google.protobuf.json_format import MessageToDict
    from pubsub import pub # type: ignore[import-untyped]

    import meshtastic.test
    import meshtastic.util
    from meshtastic import mt_config
    from meshtastic import channel_pb2, config_pb2, portnums_pb2, remote_hardware, BROADCAST_ADDR
    from meshtastic.version import get_active_version
    from meshtastic.ble_interface import BLEInterface
    from meshtastic.mesh_interface import MeshInterface

    from colorama import Fore
    from colorama import Style
except ImportError as error:
    print(f"Error : {error}")
    print("\nMake sure to run: pip install -r requirements\n")
    sys.exit(1)

bardeadas = [
    "Chupame un huevo, {frm}!",
    "No rompas los huevos, {frm}",
    "Deja de joder, {frm}",
    "Anda a laburar, {frm}",
    "Che {frm}, no rompas las pelotas",
    "Alguien está al pedo, {frm}",
    "Te dieron franco en el laburo, {frm}?",
    "Che {frm}, buscate un trabajo honesto!",
    "Andate a la esquina a ver si llueve, {frm}...",
    "Ahí lo tenés al pelotudo, {frm}...",
    "Te ganaste 2 medallas, {frm}... una por pelotudo y otra por si la perdés...",
    "La concha de la lora, {frm}...",
    "Che {frm}, me chupa un huevo!",
    "Dejen descansar, la concha de la lora, {frm}"
    "Anda a cantarle a Gardel, {frm}",
    "Che {frm}, sos más inútil que cenicero de moto",
    "Tenés menos onda que una puerta, {frm}",
    "No servís ni para espiar con una botella, {frm}",
    "Che {frm}, tenés menos luces que un barco pirata",
    "Anda a freír churros, {frm}",
    "{frm}, sos un cabeza de termo",
    "Sos un desastre con patas, {frm}",
    "Che {frm}, tenés menos vida que un vampiro",
    "Sos más lento que una tortuga en reversa, {frm}",
    "Anda a cortar el pasto, {frm}",
    "Che {frm}, sos más pesado que collar de melones",
    "Tenés menos palabras que un telegrama, {frm}",
    "{frm}, sos más aburrido que chupar un clavo",
    "Che {frm}, tenés menos futuro que un político honesto",
    "Sos un zapallo, {frm}",
    "Anda a lavar los platos, {frm}",
    "Che {frm}, tenés menos chispa que un encendedor mojado",
    "{frm}, sos un bocón",
    "Tenés menos gracia que un velorio, {frm}",
    "{frm}, sos un caradura",
    "Sos un pancho sin mostaza, {frm}",
    "{frm}, sos un queso",
    "Tenés menos suerte que un gato en un asado, {frm}",
    "Sos más torpe que una mula coja, {frm}",
    "Che {frm}, sos un zapallo relleno",
    "Tenés menos neuronas que un mosquito, {frm}",
    "Sos un cuatro de copas, {frm}",
    "Anda a contarle a tu abuela, {frm}",
    "Che {frm}, sos más feo que pisar caca descalzo",
    "Tenés menos sangre que una lombriz, {frm}",
    "Anda a cantarle a Magoya, {frm}",
    "Che {frm}, sos un marmota",
    "Sos más lento que un caracol en bajada, {frm}",
    "Sos más corto que patada de chancho, {frm}",
    "Che {frm}, sos un tarado",
    "Tenés menos brillo que un ladrillo, {frm}",
    "{frm}, sos un perejil",
    "Sos un gil, {frm}"
]


saludos_de_manana = [
    "¡Buenos días, {frm}!",
    "¡Feliz mañana, {frm}!",
    "¡Que tengas un excelente día, {frm}!",
    "¡Despierta y brilla, {frm}!",
    "¡Que tengas una mañana maravillosa, {frm}!",
    "¡Buenos días, {frm}! Que hoy sea un gran día para ti.",
    "¡Espero que tengas una mañana fantástica, {frm}!",
    "¡Buenos días, {frm}! ¡Aprovecha el día!",
    "¡Que tu mañana esté llena de alegría y energía, {frm}!",
    "¡Buen día, {frm}! Que todos tus sueños se hagan realidad hoy.",
    "Saludos cordiales y buenos días, {frm}.",
    "Buenos días, {frm}, saludos cordiales.",
    "Que tengas un día excelente, {frm}, saludos cordiales.",
    "Saludos cordiales, {frm}, que disfrutes de tu mañana.",
    "Buenos días, {frm}, recibe un cordial saludo.",
    "¡Qué alegría saludarte esta mañana, {frm}!",
    "¡Buenos días y bendiciones para ti, {frm}!",
    "¡Hola, {frm}! Te deseo una mañana espectacular.",
    "¡Buenos días, {frm}! Que este día te traiga mucha felicidad.",
    "¡Muy buenos días, {frm}! Que tengas una jornada fabulosa."
]

saludos_de_tarde = [
    "¡Buenas tardes, {frm}!",
    "¡Espero que estés teniendo una excelente tarde, {frm}!",
    "¡Qué tal tu día, {frm}? ¡Buenas tardes!",
    "¡Buenas tardes, {frm}! Que tu tarde sea muy productiva.",
    "¡Que disfrutes de una maravillosa tarde, {frm}!",
    "¡Buenas tardes, {frm}! Que continúes teniendo un día estupendo.",
    "¡Hola, {frm}! Te deseo una tarde llena de éxitos.",
    "¡Buenas tardes, {frm}! ¿Cómo va todo?",
    "¡Que tengas una tarde fantástica, {frm}!",
    "¡Buenas tardes, {frm}! Que el resto de tu día sea grandioso.",
    "Saludos cordiales y buenas tardes, {frm}.",
    "Buenas tardes, {frm}, saludos cordiales.",
    "Que tengas una excelente tarde, {frm}, saludos cordiales.",
    "Saludos cordiales, {frm}, que disfrutes de tu tarde.",
    "Buenas tardes, {frm}, recibe un cordial saludo.",
    "¡Qué alegría saludarte esta tarde, {frm}!",
    "¡Buenas tardes y bendiciones para ti, {frm}!",
    "¡Hola, {frm}! Te deseo una tarde espectacular.",
    "¡Buenas tardes, {frm}! Que esta tarde te traiga mucha felicidad.",
    "¡Muy buenas tardes, {frm}! Que tengas una jornada fabulosa."
]

saludos_de_noche = [
    "¡Buenas noches, {frm}!",
    "¡Espero que hayas tenido un excelente día, {frm}!",
    "¡Que tengas una noche tranquila y reparadora, {frm}!",
    "¡Buenas noches, {frm}! Que descanses bien.",
    "¡Que disfrutes de una noche maravillosa, {frm}!",
    "¡Buenas noches, {frm}! Que tus sueños sean dulces.",
    "¡Hola, {frm}! Te deseo una noche llena de paz.",
    "¡Buenas noches, {frm}! ¿Cómo estuvo tu día?",
    "¡Que tengas una noche fantástica, {frm}!",
    "¡Buenas noches, {frm}! Que el descanso te renueve.",
    "Saludos cordiales y buenas noches, {frm}.",
    "Buenas noches, {frm}, saludos cordiales.",
    "Que tengas una excelente noche, {frm}, saludos cordiales.",
    "Saludos cordiales, {frm}, que disfrutes de tu noche.",
    "Buenas noches, {frm}, recibe un cordial saludo.",
    "¡Qué alegría saludarte esta noche, {frm}!",
    "¡Buenas noches y bendiciones para ti, {frm}!",
    "¡Hola, {frm}! Te deseo una noche espectacular.",
    "¡Buenas noches, {frm}! Que esta noche te traiga mucha paz.",
    "¡Muy buenas noches, {frm}! Que descanses y recargues energías."
]


test_keywords = [
        "test", "prueba", "try", "ping"]

ping_keywords = ["ping"]

saludos_keywords = ["buen", "buenos", "buenas", "hola"]

info_keywords = ["info"]

last_message_time = time.time() # This way it'll take a bit to start bitching

DISRUPT_MSG_INTERVAL = 60

def get_message_for_TOD():
    current_time = datetime.now().time()
    
    if current_time >= datetime.strptime('06:00:00', '%H:%M:%S').time() and \
        current_time < datetime.strptime('12:00:00', '%H:%M:%S').time(): 
        return random.choice(saludos_de_manana)
    elif current_time >= datetime.strptime('12:00:00', '%H:%M:%S').time() and \
        current_time < datetime.strptime('18:00:00', '%H:%M:%S').time():
        return random.choice(saludos_de_tarde)
    else:
        return random.choice(saludos_de_noche)

def word_in_string(keywords, string):
    """Indicate if a word in the keywords list is included in the string."""
    for w in keywords:
        if w in string.lower():
            return True
    return False


def handle_telemetry_packet(packet, interface):
    """Handle incoming TELEMETRY packet."""
    pass

def handle_position_packet(packet, interface):
    """Handle incoming POSITION packet."""
    pass

def handle_message_packet(packet, interface):
    """Handle incoming MESSAGE packet."""
    from_id = packet["fromId"]
    frm = interface.nodes[from_id]["user"]["shortName"]

    #print("--->%r<---" % packet)
    decoded = packet.get("decoded")
    msg = decoded["text"]
    reply = None

    if msg is None or len(msg) == 0:
        return

    ch_idx = packet.get("channel", 0)
    logging.info(f"{Fore.MAGENTA}\tMessage{Style.RESET_ALL} [chan {ch_idx}] : {msg}")

    # Reply to greetings messages
    if word_in_string(saludos_keywords, msg.split()[0]):
        reply = get_message_for_TOD()
    # Reply with an 'OK' to test messages
    elif word_in_string(test_keywords, msg.split()[0].lower()):
        reply = "%s OK" % msg.split()[0]
    elif msg[0] == "/":
        # Reply to specific commands
            # Reply to specific 'ping' messages
            if word_in_string(ping_keywords, msg[1 : ].lower()):
                reply = "pong"

            elif word_in_string(info_keywords, msg[1 : ]):
                # Reply to every received message with some stats
                rxSnr = packet.get("rxSnr", 0)
                hopLimit = packet.get("hopLimit", 0)
                reply = f"rxSnr: {rxSnr} - hopLimit: {hopLimit}"
    else:
        global last_message_time

        # Get the current time in seconds since the UNIX epoch
        current_time = time.time()

        # Check if at least N minutes have passed since the last message
        if current_time - last_message_time >= DISRUPT_MSG_INTERVAL * 60:
            reply = random.choice(bardeadas)

            # Update the last message time to the current time
            last_message_time = current_time

    if reply is not None:
        logging.info(f"\t{Fore.GREEN}Reply : {Style.RESET_ALL}{reply}")
        r = interface.sendText(reply.format(frm=frm), channelIndex=ch_idx)
        #print(f"res {r}")

#switch_message = {
#        "TEXT_MESSAGE_APP" : handle_message_packet,
#}

def onReceive(packet, interface):
    """Callback invoked when a packet arrives"""
    try:
        #print("-"*80 + "\n" + repr(packet))
        decoded = packet.get("decoded")
        #logging.info(f"in onReceive() decoded:{decoded}")

        if decoded is None:
            return

        #print(repr(decoded))
        from_short_name = "<UNK>"
        try:
            from_id = packet["fromId"]
            from_short_name = interface.nodes[from_id]["user"]["shortName"]
        except KeyError as e:
            pass

        to_short_name = "<UNK>"
        try:
            to_id = packet["toId"]
            if to_id == BROADCAST_ADDR:
                to_short_name = "ALL"
            else:
                to_short_name = interface.nodes[to_id]["user"]["shortName"]
        except KeyError as e:
            pass

        port = decoded["portnum"]

        #logging.info(f"{Fore.GREEN}{port}{Style.RESET_ALL} \t: "
        #    f"{Fore.CYAN}{Style.BRIGHT}{from_short_name}{Style.RESET_ALL} " 
        #    f"-> {Fore.YELLOW}{Style.BRIGHT}{to_short_name}{Style.RESET_ALL}"
        #             )
        peers_data = \
            f"{Style.RESET_ALL}({Fore.CYAN}{Style.BRIGHT}{from_short_name}{Style.RESET_ALL} " \
            f"-> {Fore.YELLOW}{Style.BRIGHT}{to_short_name}{Style.RESET_ALL})"

        #if decoded["portnum"] != "TEXT_MESSAGE_APP"":
        #    return


        if port == "TEXT_MESSAGE_APP":
            # Text message
            #payload = decoded['payload_utf8']
            mode = "Text message"
            logging.info(
                    f"{Fore.WHITE}{Style.BRIGHT}{mode:<15} "
                    f"{peers_data:<45}{Style.RESET_ALL} ")
            handle_message_packet(packet, interface)

        elif port == "RANGE_TEST_APP":
            logging.error(f"---->{decoded}<---")
            mode = "Range Test"
            logging.info(f"{Fore.CYAN}{Style.BRIGHT}{mode:<15} {peers_data:<45}")
            pass

        elif port == "DETECTION_SENSOR_APP":
            logging.error(f"---->{decoded}<---")
            mode = "Detection Sensor"
            logging.info(f"{Fore.CYAN}{Style.BRIGHT}{mode:<15} {peers_data:<45}")
            pass

        elif port == "POSITION_APP":
            # GPS data
            position = decoded['position']
            latitude = position.get('latitude')
            longitude = position.get('longitude')
            altitude = position.get('altitude')
            mode = "Position"
            logging.info(f"{Fore.BLUE}{Style.BRIGHT}{mode:<15} {peers_data:<45}{Style.RESET_ALL} "
                         f"Latitude: {latitude}, Longitude: {longitude}, "
                         f"Altitude: {altitude}")

        elif port == "NODEINFO_APP":
            #logging.error(f"---->{decoded}<---")
            user = decoded.get("user", None)
            mode = "User Info"
            if user is None:
                logging.warning(
                    f"{Fore.YELLOW}{Style.BRIGHT}{mode:<15} {peers_data:<45}{Style.RESET_ALL} "
                    "Not available")
                return

            long_name = user.get("longName", "N/A")
            short_name = user.get("shortName", "N/A")
            hw_model = user.get("hwModel", "N/A")
            role = user.get("role", "N/A")
            logging.info(
                f"{Fore.YELLOW}{Style.BRIGHT}{mode:<15} {peers_data:<45}{Style.RESET_ALL} "
                f"Name : {long_name} ({short_name}), "
                f"Hw model : {hw_model}, Role : {role}")
            pass
        elif port == "ADMIN_APP":
            pass
        elif port == "ROUTING_APP":
            #logging.error(f"---->{decoded}<---")
            pass
        elif port == "TELEMETRY_APP":
            mode = "Telemetry"
            #
            # Telemetry data
            #
            # device_metrics {
            #     battery_level: 92
            #     voltage: 4.087
            #     channel_utilization: 6.49166679
            #     air_util_tx: 5.47711086
            # }
            #
            telemetry = decoded['telemetry']
            #logging.info(f"Telemetry : {telemetry}")

            if 'deviceMetrics' in telemetry:
                metrics = telemetry.get('deviceMetrics')
                battery_level = metrics.get('batteryLevel')
                voltage = metrics.get('voltage')
                channel_utilization = metrics.get('channelUtilization')
                air_util_tx = metrics.get('airUtilTx')

                logging.info(f"{Fore.MAGENTA}{mode:<15} {peers_data:<45}{Style.RESET_ALL} "
                             f"Voltage: {voltage}V ({battery_level}%), "
                             f"Channel util.: {channel_utilization}"
                             )

            if 'environmentMetrics' in telemetry:
                # environment_metrics {
                #  temperature: 22.9
                #  barometric_pressure: 1015.01
                #}
                metrics = telemetry.get('environmentMetrics')
                temperature = metrics.get('temperature')
                barometric_pressure = metrics.get('barometricPressure')

                logging.info(f"{Fore.MAGENTA}{mode:<15} {peers_data:<45}{Style.RESET_ALL} "
                             f"Temp: {temperature}C , Barometric Press. {barometric_pressure}{Style.RESET_ALL}"
                             )

        elif port == "REMOTE_HARDWARE_APP":
            logging.error(f"---->{decoded}<---")
            pass
        elif port == "SIMULATOR_APP":
            logging.error(f"---->{decoded}<---")
            pass
        elif port == "TRACEROUTE_APP":
            mode = "Traceroute"
            want_response = decoded.get("wantResponse", "N/A")
            logging.info(f"{Fore.RED}{mode:<15} {peers_data:<45}{Style.RESET_ALL} "
                         f"Want Response: {want_response}"
                         )
        elif port == "WAYPOINT_APP":
            logging.error(f"---->{decoded}<---")
            pass
        elif port == "PAXCOUNTER_APP":
            logging.error(f"---->{decoded}<---")
            pass
        elif port == "STORE_FORWARD_APP":
            logging.error(f"---->{decoded}<---")
            pass
        elif port == "NEIGHBORINFO_APP":
            logging.error(f"---->{decoded}<---")
            pass
        elif port == "MAP_REPORT_APP":
            logging.error(f"---->{decoded}<---")
            pass

        if 'payload_bytes' in decoded:
            # Binary data
            payload = decoded['payload_bytes']
            logging.info(f"\tBinary data {peers_data:<45} {payload}")
        elif 'data' in decoded:
            # Generic data message
            data = decoded['data']
            sensor_type = data.get('sensorType')
            value = data.get('value')
            logging.info(f"\tData message {peers_data:<45} Sensor Type: {sensor_type}, Value: {value}")
        #else:
        #    logging.info(f"\tUnknown packet from {from_short_name} to {to_short_name}")

    except KeyError as ex:
        logging.error(f"Error {ex}")
        traceback_str = traceback.format_exc()
        logging.error(f"Traceback :\n{traceback_str}")

    except TypeError as ex:
        logging.error(f"Error {ex}")
        traceback_str = traceback.format_exc()
        logging.error(f"Traceback :\n{traceback_str}")

def onConnection(interface, topic=pub.AUTO_TOPIC):  # pylint: disable=W0613
    """Callback invoked when we connect/disconnect from a radio"""
    print(f"Connection changed: {topic.getName()}")

def subscribe():
    """Subscribe to the topics the user probably wants to see, prints output to stdout"""
    pub.subscribe(onReceive, "meshtastic.receive")

def print_nodes(client):
    # Obtain and display a list of known nodes.
    for i, (node_id, node) in enumerate(client.nodes.items(), start=1):
        print(f"#{i}, Nodo ID: {node_id}, Nombre: {node['user']['longName']},")

def start(client):
    """..."""
    #print_nodes(client)
    subscribe()

    while True:
        time.sleep(3)
        if client.isConnected == False:
            logging.critical("!!!! Client disconnected !!!!")
            logging.error("--->%r<---" % client)
            break

def main():
    """Main routine."""
    logfile = None
    logging.basicConfig(
        level=logging.INFO,
        format = 
            f"{Fore.WHITE}{Style.DIM}%(asctime)s{Style.RESET_ALL} "
            f"{Fore.GREEN}{Style.BRIGHT}[%(levelname)s]{Style.RESET_ALL} %(message)s",
        datefmt='%H:%M:%S'
    )

    device = sys.argv[1]
    logging.info(f"{Fore.MAGENTA}{Style.BRIGHT}{__description__} v{__version__}{Style.RESET_ALL}")

    while True:
        try:
            logging.info(f"Connected to device  : {Fore.GREEN}{device}{Style.RESET_ALL}")
            client = meshtastic.tcp_interface.TCPInterface( device, debugOut=logfile,
                                                           noProto=None)
            start(client)
        except KeyboardInterrupt as ex:
            logging.warning(f"Leaving (CTRL-C pressed)...")
            break
        except Exception as ex:
            logging.error(f"Disconnected from device {device}. Reson : {ex}")
            logging.error("-" * 40)

    client.close()

if __name__ == "__main__":
    main()