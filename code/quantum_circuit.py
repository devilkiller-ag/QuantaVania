import pygame
import qiskit
import numpy as np

from pygame.image import load as loadImage
from settings import *


class QuantumCircuitGridBackground(pygame.sprite.Sprite):
    def __init__(self, qc_grid_model):
        super().__init__()
        self.qc_grid_model = qc_grid_model
        self.width = QUANTUM_CIRCUIT_TILE_SIZE * (self.qc_grid_model.max_columns + 2)
        self.height = QUANTUM_CIRCUIT_TILE_SIZE * (self.qc_grid_model.max_wires + 1)
        
        # BACKGROUND SURFACE
        self.qc_bg_surface = pygame.Surface((self.width, self.height))
        self.qc_bg_surface.fill(QUANTUM_CIRCUIT_COLOR_COLOR)
        self.rect = self.qc_bg_surface.get_rect()
        self.rect.inflate_ip(-WIRE_LINE_WIDTH, -WIRE_LINE_WIDTH)

    def draw_qubit_wires(self):
        for wire in range(self.qc_grid_model.num_qubits):
            x_start = QUANTUM_CIRCUIT_TILE_SIZE * 0.5
            x_end = self.width - (QUANTUM_CIRCUIT_TILE_SIZE * 0.5)
            y = (wire + 1) * QUANTUM_CIRCUIT_TILE_SIZE 
            pygame.draw.line(
                self.qc_bg_surface, 
                QUANTUM_CIRCUIT_WIRE_COLOR, 
                (x_start, y), 
                (x_end, y),
                WIRE_LINE_WIDTH
            )

    def run(self):
        # Drawing
        pygame.draw.rect(self.qc_bg_surface, QUANTUM_CIRCUIT_WIRE_COLOR, self.rect, WIRE_LINE_WIDTH)
        self.draw_qubit_wires()

class QuantumCircuitGridMarker(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.qc_bg_surface = loadImage("graphics/circuit_gates/circuit-grid-cursor.png").convert_alpha()
        self.rect = self.qc_bg_surface.get_rect()

class QuantumCircuitGridNode:
    def __init__(self, node_type, radians = 0.0, ctrl_above = -1, ctrl_below = -1, swap = -1):
        self.node_type = node_type # What Gate is at this node
        self.radians = radians # If radian != 0 then this node have a U(theta) gate; Ex:- RX, RY, RZ
        self.ctrl_above = ctrl_above # If Ctrl_above > 0; then this node is a controlled gate with the control qubit above it
        self.ctrl_below = ctrl_below # If Ctrl_below > 0; then this node is a controlled gate with the control qubit below it
        self.swap = swap # If swap != -1 then this node have a swap gate

    def __str__(self):
        string = "Type: " + str(self.node_type)
        string += ", radians: " + str(self.radians) if self.radians != 0 else ""
        string += ", ctrl_a: " + str(self.ctrl_above) if self.ctrl_above != -1 else ""
        string += ", ctrl_b: " + str(self.ctrl_below) if self.ctrl_below != -1 else ""
        return string

class QuantumCircuitGridGate(pygame.sprite.Sprite):
    def __init__(self, qc_grid_model, wire, column):
        super().__init__()
        self.qc_grid_model = qc_grid_model
        
        # Gate Position
        self.wire = wire
        self.column = column
    
    def import_gate(gate_name, colorkey = None):
        gate_image_folder = "graphics/quantum_gates"
        gate_image = loadImage(f"{gate_image_folder}/{gate_name}")
        if colorkey is not None:
            if colorkey == -1:
                colorkey = gate_image.get_at((0,0))
            gate_image.set_colorkey(colorkey)
        return gate_image, gate_image.get_rect()

    def load_gate(self):
        gate = self.qc_grid_model.get_node_gate(self.wire, self.column)
        
        if gate == GATES['IDEN']:
            self.gate_surface, self.gate_rect = self.import_gate("iden_gate.png", -1)    
        
        elif gate == GATES['X']:
            node = self.qc_grid_model.get_node(self.wire, self.column)
            # Check if this is a CNOT Gate
            if node.ctrl_above >= 0 or node.ctrl_below >= 0:
                if self.wire > max(node.ctrl_a, node.ctrl_b): # If target wire is below control wire
                    self.gate_surface, self.gate_rect = self.import_gate("not_gate_below_ctrl.png", -1)
                else: # If target wire is above control wire
                    self.gate_surface, self.gate_rect = self.import_gate("not_gate_above_ctrl.png", -1)
            elif node.radians != 0: # Else If this is a RX Gate
                self.gate_surface, self.gate_rect = self.import_gate("rx_gate.png", -1)
                # Draw the value of theta as an arc of a circle 
                pygame.draw.arc(self.gate_surface, QUANTUM_GATE_PHASE_COLOR, self.gate_rect, 0, node.radians % (2 * np.pi), 4)
            else: # Else if this is a normal X Gate
                self.gate_surface, self.gate_rect = self.import_gate("x_gate.png", -1)
        
        elif gate == GATES['Y']:
            node = self.qc_grid_model.get_node(self.wire, self.column)
            # Check if this is a RY Gate
            if node.radians != 0:
                self.gate_surface, self.gate_rect = self.import_gate("ry_gate.png", -1)
                # Draw the value of theta as an arc of a circle 
                pygame.draw.arc(self.gate_surface, QUANTUM_GATE_PHASE_COLOR, self.gate_rect, 0, node.radians % (2 * np.pi), 4)
            else: # Else if this is a normal Y Gate
                self.gate_surface, self.gate_rect = self.import_gate("y_gate.png", -1)
        
        elif gate == GATES['Z']:
            node = self.qc_grid_model.get_node(self.wire, self.column)
            # Check if this is a RY Gate
            if node.radians != 0:
                self.gate_surface, self.gate_rect = self.import_gate("rz_gate.png", -1)
                # Draw the value of theta as an arc of a circle 
                pygame.draw.arc(self.gate_surface, QUANTUM_GATE_PHASE_COLOR, self.gate_rect, 0, node.radians % (2 * np.pi), 4)
            else: # Else if this is a normal Y Gate
                self.gate_surface, self.gate_rect = self.import_gate("z_gate.png", -1)
        
        elif gate == GATES['S']:
            self.gate_surface, self.gate_rect = self.import_gate("s_gate.png", -1)
        
        elif gate == GATES['SDG']:
            self.gate_surface, self.gate_rect = self.import_gate("sdg_gate.png", -1)
        
        elif gate == GATES['T']:
            self.gate_surface, self.gate_rect = self.import_gate("t_gate.png", -1)
        
        elif gate == GATES['TDG']:
            self.gate_surface, self.gate_rect = self.import_gate("tdg_gate.png", -1)

        elif gate == GATES['H']:
            self.gate_surface, self.gate_rect = self.import_gate("h_gate.png", -1)
        
        elif gate == GATES['SWAP']:
            self.gate_surface, self.gate_rect = self.import_gate("swap_gate.png", -1)
        
        elif gate == GATES['CTRL']:
            # Check if the target wire is above the control wire
            if self.wire > self.qc_grid_model.get_control_wire_for_target_gate_at(self.wire, self.column):
                self.gate_surface, self.gate_rect = self.import_gate("ctrl_gate_bottom_wire.png", -1)
            else: # if the target wire is above the control wire
                self.gate_surface, self.gate_rect = self.import_gate("ctrl_gate_top_wire.png", -1)
        
        elif gate == GATES['CTRL_LINE']:
            self.gate_surface, self.gate_rect = self.import_gate("ctrl_line_gate.png", -1)
        
        else: # If the node is empty
            # Draw a transparent block, i.e., empty gate/node
            self.gate_surface = pygame.Surface([GATE_TILE_WIDTH, GATE_TILE_HIEGHT])
            self.gate_surface.set_alpha(0)
            self.rect = self.image.get_rect()
        
        self.gate_surface.convert()

    def run(self):
        self.load_gate()

class QuantumCircuitGridModel():
    def __init__(self, num_qubits, num_columns):
        self.num_qubits = num_qubits
        self.num_columns = num_columns
        self.nodes = np.zeros(
            (self.circuit_grid_model.max_wires, self.circuit_grid_model.max_columns),
            dtype=QuantumCircuitGridNode
        )
    
    def __str__(self):
        string = "CircuitGridModel:\n"
        for wire in range(self.num_qubits):
            row_values = [str(self.get_gate_at_node(wire, column)) for column in range(self.num_columns)]
            string += ", ".join(row_values) + "\n"
        return string

    def set_node(self, wire, column, qc_grid_node):
        self.nodes[wire][column] = QuantumCircuitGrid(
            qc_grid_node.node_type,
            qc_grid_node.radians,
            qc_grid_node.ctrl_above,
            qc_grid_node.ctrl_below,
            qc_grid_node.swap
        )

class QuantumCircuitGrid(pygame.sprite.RenderPlain):
    def __init__(self, position):
        super().__init__()
        
        ## State
        self.position = position
        self.current_wire = 0
        self.current_column = 0
        
        self.qc_grid_model = QuantumCircuitGridModel()
        self.circuit_grid_background = QuantumCircuitGridBackground()
        self.circuit_grid_background = QuantumCircuitGridMarker()

        self.gate_tiles = np.zeros(
            (self.circuit_grid_model.max_wires, self.circuit_grid_model.max_columns),
            dtype=QuantumCircuitGridGate
        )