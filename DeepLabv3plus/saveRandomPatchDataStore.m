%% creates patches from test images and saves in folder
imdsTest = imageDatastore('3_Ortho_IRRG_test','FileExtensions',{'.tif'});
pxdsTest = pixelLabelDatastore('labels_png_test',classNames,1:6);

augmenter = imageDataAugmenter('RandScale',[1 1.3],'RandXReflection',true,'RandYReflection',true);% augment
pximdsTest = randomPatchExtractionDatastore(imdsTest,pxdsTest,[1000,1000],'PatchesPerImage',20,'DataAugmentation',augmenter);% Define validation data.

tmp=read(pximdsTest);reset(pximdsTest);
% tmpImages=cell2mat(tmp.InputImage);
% tmpImages=reshape(tmpImages,1024,1024,3,[]);
for i=1:size(tmp,1)
    I = tmp.InputImage{i,1};
    imwrite(I,sprintf('test_patch/im/%d.jpg',i));
    GT = tmp.ResponsePixelLabelImage{i,1};
    GT2 = labeloverlay(zeros(size(I)),GT,'Colormap',cmap,'Transparency',0);
    imwrite(GT2,sprintf('test_patch/label/%d.png',i));
end


