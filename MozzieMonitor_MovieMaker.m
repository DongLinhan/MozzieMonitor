function MovieMaker(videoName, scaleFactor)
    %%% THis function takes the arguments ____ and makes a movie ___

    [file, path] = uigetfile('*.jpg',  'All Files (*.jpg)','MultiSelect','on');
    file = natsortfiles(file,'[-+]?\d+\.?\d*');
    
    if nargin < 2
        videoFileName = [path '/MM0005S-round2.avi'];
        scale = 1;
    else
        videoFileName = [path '/' videoName];
        scale = scaleFactor;
    end

    imageNumber = 1;
    I = imread(   [ path file{imageNumber}]     );
    [J, rect] = imcrop(I);
    J = imresize(J,scale);
    close all;


    outputVideo = VideoWriter(videoFileName);
    outputVideo.FrameRate = 30; %% how many frames are there in 1 second of video
    open(outputVideo);

    writeVideo(outputVideo,J);

    for i = 2:length(file)
        imageNumber = i;
        I = imread(   [path file{imageNumber}]     );
        J = imcrop(I, rect);
        J = imresize(J,scale);
        writeVideo(outputVideo,J);
    
    end
    close(outputVideo);
end