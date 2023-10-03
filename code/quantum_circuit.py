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
    def __init__(self, node_type, radians = 0.0, ctrl_a = -1, ctrl_b = -1, swap = -1):
        self.node_type = node_type
        self.radians = radians
        self.ctrl_a = ctrl_a
        self.ctrl_b = ctrl_b
        self.swap = swap

    def __str__(self):
        string = "Type: " + str(self.node_type)
        string += ", radians: " + str(self.radians) if self.radians != 0 else ""
        string += ", ctrl_a: " + str(self.ctrl_a) if self.ctrl_a != -1 else ""
        string += ", ctrl_b: " + str(self.ctrl_b) if self.ctrl_b != -1 else ""
        return string
