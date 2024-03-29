# Copyright (C) 2022 Georgia Tech Center for Experimental Research in Computer Systems
"""Utility Functions

This module contains utility functions that are used by notebooks and scripts for data analysis.
"""

import os
import re
import tarfile
import yaml

import pandas as pd


def get_node_names(experiment_dirpath):
  return [dirname for dirname in os.listdir(os.path.join(experiment_dirpath, "logs")) if not dirname.startswith('.')]


def get_node_containers(experiment_dirpath, node_name):
  with open(os.path.join(experiment_dirpath, "conf", "system.yml")) as system_conf_file:
    return list(yaml.load(system_conf_file, Loader=yaml.Loader)[node_name]["containers"].keys())


def get_node_vcpus(experiment_dirpath, node_name):
  with open(os.path.join(experiment_dirpath, "conf", "system.yml")) as system_conf_file:
    cpuset_cpus = list(yaml.load(system_conf_file, Loader=yaml.Loader)[node_name]["containers"].values())[0]["options"].get("cpuset-cpus", None)
    if cpuset_cpus:
      return [int(cpu) for cpu in cpuset_cpus.split(',')]
  return None


def has_cpu_interference(experiment_dirpath, node_name):
  for container in get_node_containers(experiment_dirpath, node_name):
    if re.findall("cpu_interference", container):
      return True
  return False


def get_container_option(experiment_dirpath, node_name, container, option):
  with open(os.path.join(experiment_dirpath, "conf", "system.yml")) as system_conf_file:
    system_conf = yaml.load(system_conf_file, Loader=yaml.Loader)
    try:
      return system_conf[node_name]["containers"][container]["options"][option]
    except KeyError:
      return None


def get_container_env(experiment_dirpath, node_name, container, env):
  with open(os.path.join(experiment_dirpath, "conf", "system.yml")) as system_conf_file:
    system_conf = yaml.load(system_conf_file, Loader=yaml.Loader)
    for kv in system_conf[node_name]["containers"][container]["options"]["env"]:
      if kv.split('=')[0] == env:
        return kv.split('=')[1]
  return None


def get_template_param(experiment_dirpath, node_name, template, param):
  with open(os.path.join(experiment_dirpath, "conf", "system.yml")) as system_conf_file:
    system_conf = yaml.load(system_conf_file, Loader=yaml.Loader)
    try:
      return system_conf[node_name]["templates"][template]["params"][param]
    except KeyError:
      return None


def get_node_label(experiment_dirpath, node_name):
  return "/".join(sorted(get_node_containers(experiment_dirpath, node_name)))


def get_rpc_df(experiment_dirpath):
  for node_name in get_node_names(experiment_dirpath):
    for tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        for filename in tar.getnames():
          if re.match(".*rpc(_[0-9]+)?.csv", filename):
            with tar.extractfile(filename) as csvfile:
              yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_rpc_conn_df(experiment_dirpath):
  for node_name in get_node_names(experiment_dirpath):
    for tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        for filename in tar.getnames():
          if re.match(".*rpc_conn(_[0-9]+)?.csv", filename):
            with tar.extractfile(filename) as csvfile:
              yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_rpc_call_df(experiment_dirpath):
  for node_name in get_node_names(experiment_dirpath):
    for tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        for filename in tar.getnames():
          if re.match(".*rpc_call(_[0-9]+)?.csv", filename):
            with tar.extractfile(filename) as csvfile:
              yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_query_df(experiment_dirpath):
  for node_name in get_node_names(experiment_dirpath):
    for tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        for filename in tar.getnames():
          if filename.endswith("query.csv"):
            with tar.extractfile(filename) as csvfile:
              yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_query_conn_df(experiment_dirpath):
  for node_name in get_node_names(experiment_dirpath):
    for tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        for filename in tar.getnames():
          if filename.endswith("query_conn.csv"):
            with tar.extractfile(filename) as csvfile:
              yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_query_call_df(experiment_dirpath):
  for node_name in get_node_names(experiment_dirpath):
    for tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        for filename in tar.getnames():
          if filename.endswith("query_call.csv"):
            with tar.extractfile(filename) as csvfile:
              yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_redis_df(experiment_dirpath):
  for node_name in get_node_names(experiment_dirpath):
    for tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        for filename in tar.getnames():
          if filename.endswith("redis.csv"):
            with tar.extractfile(filename) as csvfile:
              yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_loadgen_df(experiment_dirpath):
  for node_name in get_node_names(experiment_dirpath):
    for tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        for filename in tar.getnames():
          if re.match(".*loadgen([0-9]+)?.csv", filename):
            with tar.extractfile(filename) as csvfile:
              yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_collectl_cpu_df(experiment_dirpath):
  for node_name in get_node_names(experiment_dirpath):
    for tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        for filename in tar.getnames():
          if filename.endswith(".cpu.csv"):
            with tar.extractfile(filename) as csvfile:
              yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_collectl_mem_df(experiment_dirpath):
  for node_name in get_node_names(experiment_dirpath):
    for tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        for filename in tar.getnames():
          if filename.endswith(".numa.csv"):
            with tar.extractfile(filename) as csvfile:
              yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_collectl_dsk_df(experiment_dirpath):
  for node_name in get_node_names(experiment_dirpath):
    for tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        for filename in tar.getnames():
          if filename.endswith(".dsk.csv"):
            with tar.extractfile(filename) as csvfile:
              yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_cpurunq_df(experiment_dirpath):
  tarball_name = "cpurunq-bpftrace.tar.gz"
  for node_name in get_node_names(experiment_dirpath):
    if tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        if "./log.csv" in tar.getnames():
          with tar.extractfile("./log.csv") as csvfile:
            yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_cpurunqfunc_df(experiment_dirpath):
  tarball_name = "cpurunqfunc-bpftrace.tar.gz"
  for node_name in get_node_names(experiment_dirpath):
    if tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        if "./log.csv" in tar.getnames():
          with tar.extractfile("./log.csv") as csvfile:
            yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_tcpsynbl_df(experiment_dirpath):
  tarball_name = "tcpsynbl-bpftrace.tar.gz"
  for node_name in get_node_names(experiment_dirpath):
    if tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        if "./log.csv" in tar.getnames():
          with tar.extractfile("./log.csv") as csvfile:
            yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_tcpacceptq_df(experiment_dirpath):
  tarball_name = "tcpacceptq-bpftrace.tar.gz"
  for node_name in get_node_names(experiment_dirpath):
    if tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        if "./log.csv" in tar.getnames():
          with tar.extractfile("./log.csv") as csvfile:
            yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_tcpretrans_df(experiment_dirpath):
  tarball_name = "tcpretrans-bpftrace.tar.gz"
  for node_name in get_node_names(experiment_dirpath):
    if tarball_name in os.listdir(os.path.join(experiment_dirpath, "logs", node_name)):
      tarball_path = os.path.join(experiment_dirpath, "logs", node_name, tarball_name)
      with tarfile.open(tarball_path, "r:gz") as tar:
        if "./log.csv" in tar.getnames():
          with tar.extractfile("./log.csv") as csvfile:
            yield (node_name, tarball_name, pd.read_csv(csvfile, parse_dates=["timestamp"]).assign(node_name=node_name))


def get_experiment_start_time(experiment_dirpath):
  requests = pd.concat([df[2] for df in get_loadgen_df(experiment_dirpath)])
  return requests["timestamp"].values.min()


def get_experiment_end_time(experiment_dirpath):
  requests = pd.concat([df[2] for df in get_loadgen_df(experiment_dirpath)])
  return requests["timestamp"].values.max()


def get_experiment_total_duration(experiment_dirpath):
  with open(os.path.join(experiment_dirpath, "conf", "workload.yml")) as workload_conf_file:
    return yaml.load(workload_conf_file, Loader=yaml.Loader)["duration"]["total"]


def get_experiment_ramp_up_duration(experiment_dirpath):
  with open(os.path.join(experiment_dirpath, "conf", "workload.yml")) as workload_conf_file:
    return yaml.load(workload_conf_file, Loader=yaml.Loader)["duration"]["ramp_up"]


def get_experiment_ramp_down_duration(experiment_dirpath):
  with open(os.path.join(experiment_dirpath, "conf", "workload.yml")) as workload_conf_file:
    return yaml.load(workload_conf_file, Loader=yaml.Loader)["duration"]["ramp_down"]


def build_requests_df(experiment_dirpath):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath)
  # Build data frame.
  requests = pd.concat([df[2] for df in get_loadgen_df(experiment_dirpath)])
  # (Re) Build columns.
  requests["timestamp"] = requests.apply(lambda r: (r["timestamp"] - start_time).total_seconds(), axis=1)
  requests["window_1000"] = requests["timestamp"].round(0).multiply(1000)
  requests["window_10"] = requests["timestamp"].round(2).multiply(1000)
  requests["latency"] = requests["latency"].multiply(1000)
  # (Re) Create index
  requests.set_index("timestamp", inplace=True)
  requests.sort_index(inplace=True)
  return requests


def build_redis_df(experiment_dirpath):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath)
  # Build data frame.
  redis = pd.concat([df[2] for df in get_redis_df(experiment_dirpath)])
  # (Re) Build columns.
  redis["timestamp"] = redis.apply(lambda r: (r["timestamp"] - start_time).total_seconds(), axis=1)
  redis["window_10"] = redis["timestamp"].round(2).multiply(1000)
  redis["window_1000"] = redis["timestamp"].round(0).multiply(1000)
  redis["latency"] = redis["latency"].multiply(1000)
  # (Re) Create index
  redis.set_index("timestamp", inplace=True)
  redis.sort_index(inplace=True)
  return redis


def build_rpc_df(experiment_dirpath):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath)
  # Build data frame.
  rpc = pd.concat([df[2] for df in get_rpc_df(experiment_dirpath)])
  # (Re) Build columns.
  rpc["timestamp"] = rpc.apply(lambda r: (r["timestamp"] - start_time).total_seconds(), axis=1)
  rpc["window_10"] = rpc["timestamp"].round(2).multiply(1000)
  rpc["window_1000"] = rpc["timestamp"].round(0).multiply(1000)
  rpc["latency"] = rpc["latency"].multiply(1000)
  # (Re) Create index
  rpc.set_index("timestamp", inplace=True)
  rpc.sort_index(inplace=True)
  return rpc


def build_rpc_conn_df(experiment_dirpath):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath)
  # Build data frame.
  rpc_conn = pd.concat([df[2] for df in get_rpc_conn_df(experiment_dirpath)])
  # (Re) Build columns.
  rpc_conn["timestamp"] = rpc_conn.apply(lambda r: (r["timestamp"] - start_time).total_seconds(), axis=1)
  rpc_conn["window_10"] = rpc_conn["timestamp"].round(2).multiply(1000)
  rpc_conn["window_1000"] = rpc_conn["timestamp"].round(0).multiply(1000)
  rpc_conn["latency"] = rpc_conn["latency"].multiply(1000)
  # (Re) Create index
  rpc_conn.set_index("timestamp", inplace=True)
  rpc_conn.sort_index(inplace=True)
  return rpc_conn


def build_rpc_call_df(experiment_dirpath):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath)
  # Build data frame.
  rpc_call = pd.concat([df[2] for df in get_rpc_call_df(experiment_dirpath)])
  # (Re) Build columns.
  rpc_call["timestamp"] = rpc_call.apply(lambda r: (r["timestamp"] - start_time).total_seconds(), axis=1)
  rpc_call["window_10"] = rpc_call["timestamp"].round(2).multiply(1000)
  rpc_call["window_1000"] = rpc_call["timestamp"].round(0).multiply(1000)
  rpc_call["latency"] = rpc_call["latency"].multiply(1000)
  # (Re) Create index
  rpc_call.set_index("timestamp", inplace=True)
  rpc_call.sort_index(inplace=True)
  return rpc_call


def build_query_df(experiment_dirpath):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath)
  # Build data frame.
  query = pd.concat([df[2] for df in get_query_df(experiment_dirpath)])
  # (Re) Build columns.
  query["timestamp"] = query.apply(lambda r: (r["timestamp"] - start_time).total_seconds(), axis=1)
  query["window_10"] = query["timestamp"].round(2).multiply(1000)
  query["window_1000"] = query["timestamp"].round(0).multiply(1000)
  query["latency"] = query["latency"].multiply(1000)
  # (Re) Create index.
  query.set_index("timestamp", inplace=True)
  query.sort_index(inplace=True)
  return query


def build_query_conn_df(experiment_dirpath):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath)
  # Build data frame.
  query_conn = pd.concat([df[2] for df in get_query_conn_df(experiment_dirpath)])
  # (Re) Build columns.
  query_conn["timestamp"] = query_conn.apply(lambda r: (r["timestamp"] - start_time).total_seconds(), axis=1)
  query_conn["window_10"] = query_conn["timestamp"].round(2).multiply(1000)
  query_conn["window_1000"] = query_conn["timestamp"].round(0).multiply(1000)
  query_conn["latency"] = query_conn["latency"].multiply(1000)
  # (Re) Create index.
  query_conn.set_index("timestamp", inplace=True)
  query_conn.sort_index(inplace=True)
  return query_conn


def build_query_call_df(experiment_dirpath):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath)
  # Build data frame.
  query_call = pd.concat([df[2] for df in get_query_call_df(experiment_dirpath)])
  # (Re) Build columns.
  query_call["timestamp"] = query_call.apply(lambda r: (r["timestamp"] - start_time).total_seconds(), axis=1)
  query_call["window_10"] = query_call["timestamp"].round(2).multiply(1000)
  query_call["window_1000"] = query_call["timestamp"].round(0).multiply(1000)
  query_call["latency"] = query_call["latency"].multiply(1000)
  # (Re) Create index.
  query_call.set_index("timestamp", inplace=True)
  query_call.sort_index(inplace=True)
  return query_call


def build_collectl_cpu_df(experiment_dirpath):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath)
  # Build data frame.
  cpu = pd.concat([df[2] for df in get_collectl_cpu_df(experiment_dirpath)])
  # (Re) Build columns.
  cpu["timestamp"] = cpu.apply(lambda r: (r["timestamp"] - start_time).total_seconds(), axis=1)
  cpu["window_1000"] = cpu["timestamp"].round(0).multiply(1000)
  # (Re) Create index.
  cpu.set_index("timestamp", inplace=True)
  cpu.sort_index(inplace=True)
  return cpu


def build_collectl_dsk_df(experiment_dirpath):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath)
  # Build data frame.
  dsk = pd.concat([df[2] for df in get_collectl_dsk_df(experiment_dirpath)])
  # (Re) Build columns.
  dsk["timestamp"] = dsk.apply(lambda r: (r["timestamp"] - start_time).total_seconds(), axis=1)
  dsk["window_1000"] = dsk["timestamp"].round(0).multiply(1000)
  # (Re) Create index.
  dsk.set_index("timestamp", inplace=True)
  dsk.sort_index(inplace=True)
  return dsk


def build_collectl_mem_df(experiment_dirpath):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath)
  # Build data frame.
  mem = pd.concat([df[2] for df in get_collectl_mem_df(experiment_dirpath)])
  # (Re) Build columns.
  mem["timestamp"] = mem.apply(lambda r: (r["timestamp"] - start_time).total_seconds(), axis=1)
  mem["window_1000"] = mem["timestamp"].round(0).multiply(1000)
  # (Re) Create index.
  mem.set_index("timestamp", inplace=True)
  mem.sort_index(inplace=True)
  return mem


def build_cpurunq_df(experiment_dirpath, time_delta_in_s=0):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath) - pd.Timedelta(hours=6)
  # Build data frame.
  queue = pd.concat([df[2] for df in get_cpurunq_df(experiment_dirpath)])
  # (Re) Build columns.
  queue["timestamp"] = queue.apply(lambda r: (r["timestamp"] - start_time).total_seconds() + time_delta_in_s, axis=1)
  queue["window_1000"] = queue["timestamp"].round(0).multiply(1000)
  queue["window_10"] = queue["timestamp"].round(2).multiply(1000)
  queue["qlat_avg"] = queue["qlat_avg"].div(1000000.0)
  queue["qlat_max"] = queue["qlat_max"].div(1000000.0)
  # (Re) Create index.
  queue.set_index("timestamp", inplace=True)
  queue.sort_index(inplace=True)
  return queue


def build_cpurunqfunc_df(experiment_dirpath, time_delta_in_s=0):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath) - pd.Timedelta(hours=6)
  # Build data frame.
  queue = pd.concat([df[2] for df in get_cpurunqfunc_df(experiment_dirpath)])
  # (Re) Build columns.
  queue["timestamp"] = queue.apply(lambda r: (r["timestamp"] - start_time).total_seconds() + time_delta_in_s, axis=1)
  queue["window_1000"] = queue["timestamp"].round(0).multiply(1000)
  queue["window_10"] = queue["timestamp"].round(2).multiply(1000)
  queue["qlat_avg"] = queue["qlat_avg"].div(1000000.0)
  queue["qlat_max"] = queue["qlat_max"].div(1000000.0)
  # (Re) Create index.
  queue.set_index("timestamp", inplace=True)
  queue.sort_index(inplace=True)
  return queue


def build_tcpsynbl_df(experiment_dirpath, time_delta_in_s=0):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath) - pd.Timedelta(hours=6)
  # Build data frame.
  synbl = pd.concat([df[2] for df in get_tcpsynbl_df(experiment_dirpath)])
  # (Re) Build columns.
  synbl["timestamp"] = synbl.apply(lambda r: (r["timestamp"] - start_time).total_seconds() + time_delta_in_s, axis=1)
  synbl["window_1000"] = synbl["timestamp"].round(0).multiply(1000)
  synbl["window_10"] = synbl["timestamp"].round(2).multiply(1000)
  synbl["synbl_lat_avg"] = synbl["synbl_lat_avg"].div(1000000.0)
  synbl["synbl_lat_max"] = synbl["synbl_lat_max"].div(1000000.0)
  # (Re) Create index.
  synbl.set_index("timestamp", inplace=True)
  synbl.sort_index(inplace=True)
  return synbl


def build_tcpacceptq_df(experiment_dirpath, time_delta_in_s=0):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath) - pd.Timedelta(hours=6)
  # Build data frame.
  acceptq = pd.concat([df[2] for df in get_tcpacceptq_df(experiment_dirpath)])
  # (Re) Build columns.
  acceptq["timestamp"] = acceptq.apply(lambda r: (r["timestamp"] - start_time).total_seconds() + time_delta_in_s, axis=1)
  acceptq["window_1000"] = acceptq["timestamp"].round(0).multiply(1000)
  acceptq["window_10"] = acceptq["timestamp"].round(2).multiply(1000)
  acceptq["acceptq_lat_avg"] = acceptq["acceptq_lat_avg"].div(1000000.0)
  acceptq["acceptq_lat_max"] = acceptq["acceptq_lat_max"].div(1000000.0)
  # (Re) Create index.
  acceptq.set_index("timestamp", inplace=True)
  acceptq.sort_index(inplace=True)
  return acceptq


def build_tcpretrans_df(experiment_dirpath, time_delta_in_s=0):
  # Extract experiment information.
  start_time = get_experiment_start_time(experiment_dirpath) - pd.Timedelta(hours=6)
  # Build data frame.
  retrans = pd.concat([df[2] for df in get_tcpretrans_df(experiment_dirpath)])
  # (Re) Build columns.
  retrans["timestamp"] = retrans.apply(lambda r: (r["timestamp"] - start_time).total_seconds() + time_delta_in_s, axis=1)
  retrans["window_1000"] = retrans["timestamp"].round(0).multiply(1000)
  retrans["window_10"] = retrans["timestamp"].round(2).multiply(1000)
  # (Re) Create index.
  retrans.set_index("timestamp", inplace=True)
  retrans.sort_index(inplace=True)
  return retrans
