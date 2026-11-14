# Source verification — Lucas–Kanade optical flow

## Identity and bibliography
Lucas, B. D., & Kanade, T. (1981), “An Iterative Image Registration Technique with an Application to Stereo Vision,” Proceedings of IJCAI-81, pp. 674–679. The IJCAI proceedings entry identifies the authors, conference, pages and original method.

## Technical claims checked
The primary paper develops gradient-directed image registration and a local linear approximation for matching. The optical-flow teaching baseline uses the corresponding local brightness-constancy least-squares constraint and structure-tensor conditioning. It is not a faithful implementation of the paper's iterative registration procedure.

## Implementation and reproduction
Tests use a synthetic subpixel horizontal translation, identical images, a flat region and invalid input. The code returns dense flow and a validity mask. It does not provide pyramids, warping, feature selection, occlusion handling or advanced dense-flow algorithms. Run repository tests and CI independently.

## Rights
Only bibliographic metadata and paraphrased mathematics are included; no figures or paper text are copied.
