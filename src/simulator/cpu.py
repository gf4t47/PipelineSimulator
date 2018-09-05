"""
  Copyright (C) 2018 Kenneth Lee. All rights reserved.
  Modifications copyright (C) 2018 <Laserfiche/Kern Ding>

 TLicensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

from src.simulator.instruction import inst_set, DATA_MEMORY_BOUNDARY
from src.util.log import log_err


class Cpu:
    def __init__(self, mem: bytearray)->None:
        self._pc = 0
        self._reg = [0] * 12
        self._pstate = 0
        self._mem = mem

    @property
    def pc(self)->int:
        return self._pc

    @pc.setter
    def pc(self, value: int)->None:
        self._pc = value

    @property
    def pstate(self)->int:
        return self._pstate

    @pstate.setter
    def pstate(self, value: int):
        self._pstate = value

    @property
    def register(self)->[int]:
        return self._reg

    @property
    def memory(self)->bytearray:
        return self._mem

    def _fetch(self)->bytearray:
        """
        get one instruction from memory
        :return: instruction
        """
        if self.pc < 0 or self.pc > DATA_MEMORY_BOUNDARY:
            log_err(f"sys abort due to invalid pc: {self.pc}")

        op = self.memory[self.pc]
        if op >= len(inst_set):
            log_err(f"sys abort due to invalid inst op: {op}")

        return self.memory[self.pc: self.pc + 4]

    def run(self, max_step: int):
        """
        execute binary instructions from memory
        :param max_step:
        :return:
        """
        count_step = 0
        while count_step < max_step:
            inst = self._fetch()
            _, inst_handler = inst_set[inst[0]]
            self.pc += inst_handler(self, inst)
            count_step += 1
        log_err(f"cpu too hot ({max_step}), exit")
