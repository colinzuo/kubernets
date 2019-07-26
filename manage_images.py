import logging
import subprocess
import sys
import argparse
import os
import json


logging.basicConfig(format='%(asctime)s  %(levelname)-8s [%(name)s] %(message)s',
                level=logging.INFO)


action_list = ['pull', 'tag', 'save', 'load', 'push', 'rm']


def handle_arguments(cl_arguments):
  parser = argparse.ArgumentParser(description='')
  # Configuration files
  parser.add_argument('--config_file', '-c', type=str, nargs="?",
                      help="config file about things such as images", required=True)
  parser.add_argument('--target_registry', '-r', type=str, nargs="?",
                      help="target_registry to act on", required=True)
  parser.add_argument('--action', '-a', type=str, nargs="?",
                      help="action_list: %s" % action_list, required=True)

  return parser.parse_args(cl_arguments)


def run_cmd(in_cmd):
    logging.info("to execute: %s" % in_cmd)
    subprocess.call(in_cmd, shell=True)


def pull_images(in_config):
    for item_lvl1 in in_config:
        for image in item_lvl1["image_list"]:
            logging.info("")
            logging.info("")
            if item_lvl1["registry"]:
                cmd = "docker pull %s/%s" % (item_lvl1["registry"], image)
            else:
                cmd = "docker pull %s" % (image,)
            run_cmd(cmd)


def tag_images(in_config, target_registry):
    for item_lvl1 in in_config:
        for image in item_lvl1["image_list"]:
            logging.info("")
            logging.info("")
            if item_lvl1["registry"]:
                cmd = "docker tag %s/%s %s/%s" % (item_lvl1["registry"], image, target_registry, image)
            else:
                cmd = "docker tag %s %s/%s" % (image, target_registry, image)
            if "@" in image:
                logging.info("@ contained, please manually tag: ref cmd %s" % cmd)
                continue
            run_cmd(cmd)


def save_images(in_config, target_registry):
    for item_lvl1 in in_config:
        for image in item_lvl1["image_list"]:
            tar_path = "%s_%s.tar" % (target_registry.replace("/", "__"), image)
            if os.path.exists(tar_path):
                logging.info("skip %s as already exist" % tar_path)
            else:
                logging.info("")
                logging.info("")
                cmd = "docker save %s/%s -o %s" % (target_registry, image, tar_path)
                run_cmd(cmd)


def load_images(in_config, target_registry):
    for item_lvl1 in in_config:
        for image in item_lvl1["image_list"]:
            logging.info("")
            logging.info("")
            cmd = "docker load -i %s_%s.tar" % (target_registry.replace("/", "__"), image)
            run_cmd(cmd)


def push_images(in_config, target_registry):
    for item_lvl1 in in_config:
        for image in item_lvl1["image_list"]:
            logging.info("")
            logging.info("")
            cmd = "docker push %s/%s" % (target_registry, image)
            if "@" in image:
                logging.info("@ contained, please manually push: ref cmd %s" % cmd)
                continue
            run_cmd(cmd)


def rm_images(in_config, target_registry):
    for item_lvl1 in in_config:
        for image in item_lvl1["image_list"]:
            logging.info("")
            logging.info("")
            cmd = "docker rmi %s/%s" % (target_registry, image)
            run_cmd(cmd)


if __name__ == '__main__':
    cl_args = handle_arguments(sys.argv[1:])

    if not cl_args.action in action_list:
        logging.error("invalid action: %s, should be one of %s" % (cl_args.action, action_list))
        sys.exit(-1)

    in_target_registry = cl_args.target_registry

    with open(cl_args.config_file) as f:
        config_map = json.load(f)

    if not "images" in config_map:
        logging.error("images must be specified in config file")
        sys.exit(-2)

    image_list = config_map['images']

    if cl_args.action == "pull":
        pull_images(image_list)

    if cl_args.action == "tag":
        tag_images(image_list, in_target_registry)

    if cl_args.action == "save":
        save_images(image_list, in_target_registry)

    if cl_args.action == "load":
        load_images(image_list, in_target_registry)

    if cl_args.action == "push":
        push_images(image_list, in_target_registry)

    if cl_args.action == "rm":
        rm_images(image_list, in_target_registry)
