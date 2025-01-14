#!/bin/bash

lines=3
rm run21_mb_dst_truth_jet_* run21_mb_dst_global_* run21_mb_dst_calo_cluster_* run21_mb_dst_truthinfo_*
args="-l $lines --numeric-suffixes=0 --suffix-length=4 --additional-suffix=.list"
split $args run21_mb_dst_truth_jet.list "run21_mb_dst_truth_jet_"
split $args run21_mb_dst_global.list "run21_mb_dst_global_"
split $args run21_mb_dst_calo_cluster.list "run21_mb_dst_calo_cluster_"
split $args run21_mb_dst_truthinfo.list "run21_mb_dst_truthinfo_"