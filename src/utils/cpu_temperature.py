def get_cpu_temperatures():
    import wmi

    temps = []
    w = wmi.WMI(namespace="root\\wmi")

    for sensor in w.MSAcpi_ThermalZoneTemperature():
        # tenths of Kelvin → Celsius
        temp_c = (sensor.CurrentTemperature / 10) - 273.15
        if temp_c > 0:
            temps.append(temp_c)

    return temps