import os

from migen import *

from litex.soc.interconnect import wishbone


class Minerva(Module):
    name = "minerva"
    endianness = "little"
    gcc_triple = ("riscv64-unknown-elf", "riscv32-unknown-elf")
    gcc_flags = "-D__minerva__ -march=rv32i -mabi=ilp32"
    linker_output_format = "elf32-littleriscv"

    def __init__(self, platform, cpu_reset_address, variant=None):
        assert variant is None, "Unsupported variant %s" % variant
        self.reset = Signal()
        self.ibus = wishbone.Interface()
        self.dbus = wishbone.Interface()
        self.interrupt = Signal(32)

        ###

        ports = {
            "i_clk": ClockSignal(),
            "i_rst": ResetSignal() | self.reset,
            "i_external_interrupt": self.interrupt,

            "o_ibus_adr": self.ibus.adr,
            "o_\\ibus_dat_w$5 ": self.ibus.dat_w,
            "o_\\ibus_sel$6 ": self.ibus.sel,
            "o_ibus_cyc": self.ibus.cyc,
            "o_ibus_stb": self.ibus.stb,
            "o_\\ibus_we$7 ": self.ibus.we,
            "o_ibus_cti": self.ibus.cti,
            "o_ibus_bte": self.ibus.bte,
            "i_ibus_dat_r": self.ibus.dat_r,
            "i_ibus_ack": self.ibus.ack,
            "i_ibus_err": self.ibus.err,

            "o_dbus_adr": self.dbus.adr,
            "o_dbus_dat_w": self.dbus.dat_w,
            "o_dbus_sel": self.dbus.sel,
            "o_dbus_cyc": self.dbus.cyc,
            "o_dbus_stb": self.dbus.stb,
            "o_dbus_we": self.dbus.we,
            "o_\\dbus_cti$9 ": self.dbus.cti,
            "o_\\dbus_bte$8 ": self.dbus.bte,
            "i_dbus_dat_r": self.dbus.dat_r,
            "i_dbus_ack": self.dbus.ack,
            "i_dbus_err": self.dbus.err
        }

        self.specials += Instance("minerva_cpu", **ports)
        self.add_sources(platform, variant)

        # try: # FIXME: workaround until Minerva code is released
        #     from minerva.core import Minerva as MinervaCPU
        #     self.submodules.cpu = MinervaCPU(reset_address=cpu_reset_address)
        #     self.comb += [
        #         self.cpu.reset.eq(self.reset),
        #         self.cpu.external_interrupt.eq(self.interrupt),
        #         self.cpu.ibus.connect(self.ibus),
        #         self.cpu.dbus.connect(self.dbus)
        #     ]
        # except ModuleNotFoundError:
        #     pass

    @staticmethod
    def add_sources(platform, variant):
        vdir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "verilog")
        platform.add_sources(os.path.join(vdir), "minerva.v")
