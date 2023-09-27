from threading import Thread
import krpc
import time

ESTAGIO_INICIAL = 5.0

conn = krpc.connect(
    name='Suborbital',
    address='192.168.3.155',
    rpc_port=50000,
    stream_port=50001)

vessel = conn.space_center.active_vessel

vessel.auto_pilot.target_pitch_and_heading(90, 90)
vessel.auto_pilot.engage()
vessel.control.throttle = 1

print('Ignição 1 Estágio')
vessel.control.activate_next_stage()

inclinacao = 90

while True:
    if (vessel.flight().mean_altitude > 1000 and vessel.flight().mean_altitude < 50000 and inclinacao > 45):
        vessel.auto_pilot.target_pitch_and_heading(inclinacao, 90)
        inclinacao -= 3
        print('Inclinação: ' + str(inclinacao))
        time.sleep(1)

    if (vessel.flight().mean_altitude > 50000 or vessel.orbit.apoapsis_altitude > 70000):
        vessel.auto_pilot.target_pitch_and_heading(0, 90)

    # 2º Estágio
    if (vessel.resources.amount('SolidFuel') < 1 and vessel.control.current_stage == ESTAGIO_INICIAL):
        time.sleep(5)
        print('Ignição 2 Estágio')
        vessel.control.activate_next_stage()

    # 3º Estágio
    if (vessel.resources_in_decouple_stage < 1 and vessel.control.current_stage == (ESTAGIO_INICIAL - 1)):
        time.sleep(5)
        print('Ignição 3 Estágio')
        vessel.control.activate_next_stage()
