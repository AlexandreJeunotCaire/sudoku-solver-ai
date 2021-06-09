import argparse

train_args = argparse.ArgumentParser()
train_args.add_argument("-e", "--epochs",type=int, required=True, help="Amount of epochs to perform")
train_args.add_argument("-s", "--savepath",type=str, required=True, help="Where the trained model should be saved")
train_args.add_argument("-d", "--dataset",type=str, required=True, help="Path to dataset class directories root")
train_args.add_argument("-b", "--batchsize",type=int, required=False, help="Batch size for the training (default=32)", default=32)


inference_args = argparse.ArgumentParser()
inference_inputs = inference_args.add_mutually_exclusive_group(required=True)
inference_inputs.add_argument("-i", "--image",type=str, help="Run inference on a single image")
inference_inputs.add_argument("-f", "--folder",type=str, help="Run inference on a folder")
inference_args.add_argument("-m", "--model", required=True,type=str, help="Inferencec model") 