import logging
import subprocess
import sys
import argparse


logging.basicConfig(format='%(asctime)s  %(levelname)-8s [%(name)s] %(message)s',
                level=logging.INFO)


def handle_arguments(cl_arguments):
  parser = argparse.ArgumentParser(description='')
  # Configuration files
  parser.add_argument('--target_registry', '-r', type=str, nargs="?",
                      help="target_registry to act on", required=True)
  parser.add_argument('--action', '-c', type=str, nargs="?",
                      help="save or load or rm", required=True)

  return parser.parse_args(cl_arguments)


save_config_2019_03_14 = [
    {
        "registry": "k8s.gcr.io",
        "image_list": ["kube-proxy:v1.13.4",
                       "kube-scheduler:v1.13.4",
                       "kube-apiserver:v1.13.4",
                       "kube-controller-manager:v1.13.4",
                       "pause:3.1",
                       "etcd:3.2.24",
                       "coredns:1.2.6"]
    },
    {
        "registry": "calico",
        "image_list": ["node:v3.3.5",
                       "cni:v3.3.5"]
    }
]


def run_cmd(in_cmd):
    logging.info("to execute: %s" % in_cmd)
    subprocess.call(in_cmd, shell=True)


def save_images(in_config, target_registry):
    for item_lvl1 in in_config:
        for image in item_lvl1["image_list"]:
            logging.info("")
            logging.info("")
            cmd = "docker tag %s/%s %s/%s" % (item_lvl1["registry"], image, target_registry, image)
            run_cmd(cmd)
            cmd = "docker save %s/%s -o %s_%s.tar" % (target_registry, image, target_registry, image)
            run_cmd(cmd)


def load_images(in_config, target_registry):
    for item_lvl1 in in_config:
        for image in item_lvl1["image_list"]:
            logging.info("")
            logging.info("")
            cmd = "docker load -i %s_%s.tar" % (target_registry, image)
            run_cmd(cmd)
            # cmd = "docker push %s/%s" % (target_registry, image)
            # run_cmd(cmd)


def rm_images(in_config, target_registry):
    for item_lvl1 in in_config:
        for image in item_lvl1["image_list"]:
            logging.info("")
            logging.info("")
            cmd = "docker rmi %s/%s" % (target_registry, image)
            run_cmd(cmd)


if __name__ == '__main__':
    cl_args = handle_arguments(sys.argv[1:])

    if not cl_args.action in ["save", "load", "rm"]:
        logging.error("invalid action: %s" % cl_args.action)
        sys.exit(-1)

    in_target_registry = cl_args.target_registry

    if cl_args.action == "save":
        save_images(save_config_2019_03_14, in_target_registry)

    if cl_args.action == "load":
        load_images(save_config_2019_03_14, in_target_registry)

    if cl_args.action == "rm":
        rm_images(save_config_2019_03_14, in_target_registry)
