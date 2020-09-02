from Client import Client

class CMD_Interface:

    def __init__(self):
        self.check_help_message = "Wrong Command. Please check HELP"

    def process_input(self, input_string):
        command_list = input_string.split()
        command_list[0] = command_list[0].upper()
        for i in range(1, len(command_list)):
            try:
                command_list[i] = int(command_list[i])
            except:
                if (command_list[i][0] == '"' or command_list[i][0] == "'"):
                    if command_list[i][-1] != command_list[i][0]:
                        command_list[0] = 'help'   # Prompts the program to print the HELP message
                    command_list[i] = command_list[i][1 : -1]

        return command_list

    def print_help(self):
        print("""Please enter one of the following commands in one line
                    GET 'key'
                    SET 'key' 'value'
                    DELETE 'key'
                    FLUSH
                """)

    def run_client_with_command_list(self, c, command_list):
        if len(command_list) == 1:
            if command_list[0] == 'FLUSH':
                return c.execute(command_list[0])
            else:
                return self.check_help_message

        elif len(command_list) == 2:
            if command_list[0] == 'GET' or command_list[0] == 'DELETE':
                return c.execute(command_list[0], command_list[1])
            else:
                return self.check_help_message

        elif len(command_list) == 3:
            if command_list[0] == 'SET':
                return c.execute(command_list[0], command_list[1], command_list[2])
            else:
                return self.check_help_message

        else:
            return self.check_help_message

    def run(self):
        c = Client()
        print("If you don't know what to do, please enter HELP")
        while True:

            input_string = input("Please enter the command\n")
            command_list = self.process_input(input_string)

            if command_list[0] != 'GET' and command_list[0] != 'SET' and command_list[0] != 'DELETE' and command_list[0] != 'FLUSH':
                self.print_help()
                continue

            response = self.run_client_with_command_list(c, command_list)
            print(response)

if __name__ == "__main__":
    cmd_interface = CMD_Interface()
    cmd_interface.run()