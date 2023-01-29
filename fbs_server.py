import spacestream

fbs_client = FrameBufferSharingServer.create("TDSyphonSpoutOut")

if threading.current_thread() is threading.main_thread():
    self.fbs_client.setup()