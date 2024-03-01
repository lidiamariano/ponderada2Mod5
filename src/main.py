from serial.tools import list_ports
import pydobot
import typer
import inquirer
from yaspin import yaspin


app = typer.Typer()
available_ports = list_ports.comports()

print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[0].device

device = pydobot.Dobot(port=port, verbose=False)
velocidade = device.speed(500, 500)



@app.command()
def deviceFunction():
        continuar = True
        while continuar:
                perguntas =[inquirer.List("menu", message="O que você quer que o robô faça?", choices=["Mover para home", "Ligar ferramenta", "Desligar ferramenta", "Mover", "Posição atual"])]

                respostas = inquirer.prompt(perguntas)
                spinner = yaspin (text="O robô está iniciando", color="magenta")
                # spinner.start()
                saida = processar(respostas, device)
                # spinner.stop()
                print(saida)
        device.close()

def processar(dados, device):
    menu = dados["menu"]
    if menu == "Mover para home":
           device.move_to(240.22, 0, 150, 0, wait=True)
    elif menu == "Ligar ferramenta":
           device.suck(True)
           device.wait(200)
    elif menu == "Desligar ferramenta":
           device.suck(False)
           device.wait(200)
    elif menu == "Posição atual":
           posicao_atual = device.pose()
           print(f"Posição atual: {posicao_atual}")
    elif menu == "Mover":
            posicoes = [inquirer.List("movimento", message="Para qual direção você deseja mover o robô?", choices=["x", "y", "z", "r"])]

            respostas = inquirer.prompt(posicoes)
            spinner = yaspin(text="O robô está iniciando...", color="magenta")
            # spinner.start()
            saida = movimentos(respostas, device)
            # spinner.stop()
            print(saida)

def movimentos(direcoes, device):
    movimento=direcoes["movimento"]
    posicao_atual = device.pose()

    if movimento == "x":
        x = inquirer.prompt([inquirer.Text("x", message="Digite a posição x: ")])["x"]
        device.move_to(posicao_atual[0]+int(x), posicao_atual[1], posicao_atual[2], posicao_atual[3], wait= True)
    elif movimento == "y":
        y = inquirer.prompt([inquirer.Text("y", message="Digite a posição y: ")])["y"]
        device.move_to(posicao_atual[0], posicao_atual[1]+int(y), posicao_atual[2], posicao_atual[3], wait=True)
    elif movimento == "z":
        z = inquirer.prompt([inquirer.Text("z", message="Digite a posição z: ")])["z"]
        device.move_to(posicao_atual[0], posicao_atual[1], posicao_atual[2]+int(z), posicao_atual[3], wait=True)
    elif movimento == "r":
        r = inquirer.prompt([inquirer.Text("r", message="Digite a posição r: ")])["r"]
        device.move_to(posicao_atual[0], posicao_atual[1], posicao_atual[2], posicao_atual[3]+int(r), wait=True)

if __name__ == "__main__":
    app()
    


