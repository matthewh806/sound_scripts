import pygame, pygame.midi

midi_map = {
    144: "note_on",
    145: "note_on",
    128: "note_off",
    129: "note_off",
    177: "CC"
}


def print_device_info():
    c = pygame.midi.get_count()
    print "{} midi devices found".format(c)
    for i in range(c):
        (interf, name, input, output, opened) = pygame.midi.get_device_info(i)

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print "{}: interface :{}:, name :{}:, opened :{}:  {}".format(i, interf, name, opened, in_out)


def input_main(device_id = None):
    pygame.fastevent.init()
    event_get = pygame.fastevent.get

    if pygame.midi.get_count() == 0:
        print "Number of Midi input devices is 0. Exiting..."
        return

    print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print "using input_id :{}:".format(input_id)
    i = pygame.midi.Input(input_id)

    pygame.display.set_mode((1,1))

    going = True
    while going:
        events = event_get()
        for e in events:
            if e.type == pygame.QUIT:
                going = False
                break

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    going = False
                    break

            if e.type in [pygame.midi.MIDIIN]:
                print (e)

        if i.poll():
            midi_events = i.read(10)

            for m_e in midi_events:
                data = m_e[0]
                print "Status: {}, Note: {}, Velocity: {}".format(
                    midi_map[data[0]],
                    data[1],
                    data[2]
                )

    del i
    pygame.midi.quit()

if __name__ == "__main__":
    pygame.init()
    pygame.midi.init()
    input_main()