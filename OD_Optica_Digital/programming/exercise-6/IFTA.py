# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright Prof. LUIS MIGUEL SANCHEZ BREA with permission (e-mail to ucm.es email on November 3, 2022 at 10:10:58 GMT+1)

from copy import deepcopy

from diffractio import mm, np, plt
from diffractio.scalar_masks_XY import Scalar_mask_XY
from diffractio.scalar_sources_XY import Scalar_source_XY


def GS_far_algorithm_deprecated(source, target, num_steps, has_draw=False):
    """Gerbech-Saxton algorithm for the far field.

    Arguments:
        source (None or Scalar_field_XY): Illumination.
        target (Scalar_mask_XY): Objective.
        num_steps (int): number of steps in the algorithm
        has_draw (bool): If True, draws the errors.

    Returns:
        mask_final (Scalar_mask_XY): Result mask of algorithm.
        errors (np.array): Data of errors
    """

    x = target.x
    y = target.y
    wavelength = target.wavelength
    num_x = len(x)
    num_y = len(y)

    errors = np.zeros(num_steps)

    if source is None:
        source = Scalar_source_XY(x, y, wavelength)
        source.plane_wave()

    DOE = Scalar_mask_XY(x, y, wavelength)
    far_field = Scalar_mask_XY(x, y, wavelength)

    target_abs = np.fft.fftshift(np.abs(target.u))
    far_field.u = target_abs * np.exp(1j * 2 * np.pi * np.random.rand(num_y, num_x))
    I_result = target_abs**2
    I_result_mean = I_result.mean()

    for i in range(num_steps):
        DOE = far_field.ifft(shift=False, new_field=True)
        mask = np.angle(DOE.u)
        DOE.u = np.exp(1j * mask)
        field_z = DOE.fft(shift=False, matrix=True)
        I_z = np.abs(field_z) ** 2
        far_field.u = target_abs * np.exp(1j * np.angle(field_z))

        error = nmse(I_result, I_z)
        print("{}/{} - error {:2.6f} %".format(i, num_steps, error), end="\r")
        errors[i] = error

    mask = np.fft.fftshift(mask)
    mask = (mask + np.pi) / (2 * np.pi)

    mask_final = Scalar_mask_XY(x, y, wavelength)
    mask_final.u = mask

    if has_draw:
        plt.figure()
        plt.plot(errors, "k", lw=2)
        plt.xlabel("# step")
        plt.ylabel("error")
        plt.title("optimization")
        plt.ylim(ymin=0)

    return DOE, mask_final, errors


def insert_pupil(self, pos=None, radius=None):
    """Place a circle around the mask. It is useful for circular targets.
    It has been implemented in new version of dfifractio.py

    Arguments:
        pos (None or np.array): center of pupil.
        radius (None or np.array): radius of pupil.
    """
    if pos is None:
        posx = (self.x[-1] + self.x[0]) / 2
        posy = (self.y[-1] + self.y[0]) / 2
        pos = (posx, posy)

    if radius is None:
        radiusx = (self.x[-1] - self.x[0]) / 2
        radiusy = (self.y[-1] - self.y[0]) / 2
        radius = (radiusx, radiusy)

    pupil = Scalar_mask_XY(self.x, self.y, self.wavelength)
    pupil.circle(r0=pos, radius=radius)

    self.u = self.u * pupil.u
    return self


def GS_far_algorithm(source, target, num_steps, has_draw=False):
    """Gerbech-Saxton algorithm for the far field.

    Arguments:
        source (None or Scalar_field_XY): Illumination.
        target (Scalar_mask_XY): Objective.
        num_steps (int): number of steps in the algorithm
        has_draw (bool): If True, draws the errors.

    Returns:
        mask_final (Scalar_mask_XY): Result mask of algorithm.
        errors (np.array): Data of errors
    """

    errors = np.zeros(num_steps)

    z = 1 * mm
    x = target.x
    y = target.y
    num_x = len(x)
    num_y = len(y)
    wavelength = target.wavelength

    radius_x = (x.max() - x.min()) / 2
    radius_y = (y.max() - y.min()) / 2
    x_mean = (x.max() + x.min()) / 2
    y_mean = (y.max() + y.min()) / 2

    circle = Scalar_mask_XY(x, y, wavelength)

    if source is None:
        source = Scalar_source_XY(x, y, wavelength)
        source.plane_wave()

    DOE = Scalar_mask_XY(x, y, wavelength)
    far_field = Scalar_mask_XY(x, y, wavelength)

    target_abs = np.fft.fftshift(np.abs(target.u))
    far_field.u = target_abs * np.exp(1j * 2 * np.pi * np.random.rand(num_y, num_x))
    I_result = target_abs**2
    I_result_mean = I_result.mean()

    for i in range(num_steps):
        print("{}/{}".format(i, num_steps), end="\r")
        DOE = far_field.ifft(z=z, shift=False, new_field=True)
        mask = np.angle(DOE.u)
        DOE.u = np.exp(1j * mask)
        field_z = DOE.fft(z=z, shift=False, matrix=True)
        I_z = np.abs(field_z) ** 2
        I_z = I_z * I_result_mean / I_z.mean()
        far_field.u = target_abs * np.exp(1j * np.angle(field_z))

        error = nmse(I_result, I_z)
        print("{}/{} - error {:2.6f}".format(i, num_steps, error), end="\r")
        errors[i] = error

    if has_draw:
        plt.figure()
        plt.imshow(I_result)
        plt.colorbar()
        plt.figure()
        plt.imshow(I_z)
        plt.colorbar()
    if has_draw:
        plt.plot(errors, "k", lw=2)
        plt.xlabel("# step")
        plt.ylabel("error")
        plt.title("optimization")
        plt.ylim(ymin=0)

    mask = np.fft.fftshift(mask)
    mask = (mask + np.pi) / (2 * np.pi)

    mask_final = Scalar_mask_XY(x, y, wavelength)
    mask_final.u = mask

    return mask_final, errors


def GS_Fresnel_algorithm(source, target, z, num_steps, has_draw=False):
    """Gerbech-Saxton algorithm for the near field.

    Arguments:
        source (None or Scalar_field_XY): Illumination.
        target (Scalar_mask_XY): Objective.
        num_steps (int): number of steps in the algorithm
        has_draw (bool): If True, draws the errors.

    Returns:
        mask_final (Scalar_mask_XY): Result mask of algorithm.
        errors (np.array): Data of errors
    """

    errors = np.zeros(num_steps)

    x = target.x
    y = target.y
    wavelength = target.wavelength
    num_x = len(x)
    num_y = len(y)

    radius_x = (x.max() - x.min()) / 2
    radius_y = (y.max() - y.min()) / 2
    x_mean = (x.max() + x.min()) / 2
    y_mean = (y.max() + y.min()) / 2

    circle = Scalar_mask_XY(x, y, wavelength)
    circle.circle(r0=(x_mean, y_mean), radius=(radius_x, radius_y))

    if source is None:
        source = Scalar_source_XY(x, y, wavelength)
        source.plane_wave()

    DOE = Scalar_mask_XY(x, y, wavelength)
    field_z = Scalar_mask_XY(x, y, wavelength)
    # DOE.u=np.abs(target.u)*np.exp(1j*2*np.pi*np.random.rand(num_x,num_y))

    u_target = np.abs(target.u)
    I_result = np.abs(target.u) ** 2
    I_result_mean = I_result.mean()

    field_z.u = u_target * np.exp(2j * np.pi * np.random.rand(num_y, num_x))

    for i in range(num_steps):
        print("{}/{}".format(i, num_steps), end="\r")
        DOE = field_z.RS(z=-z, new_field=True)
        mask = np.angle(DOE.u)
        DOE.u = np.exp(1j * mask)
        field_z = (source * DOE).RS(z=z, new_field=True)
        I_z = np.abs(field_z.u) ** 2
        I_z = I_z * I_result_mean / I_z.mean()

        field_z.u = u_target * np.exp(1j * np.angle(field_z.u))

        # if has_mask:
        #     DOE.u=np.exp(1j*np.pi*mask)*circle.u

        error = nmse(I_result, I_z)
        print("{}/{} -  error {:2.6f}".format(i, num_steps, error), end="\r")
        errors[i] = error
    mask = (mask + np.pi) / (2 * np.pi)
    print(mask.max(), mask.min())

    if has_draw:
        plt.plot(errors, "k", lw=2)
        plt.title("errors")

    mask_final = Scalar_mask_XY(x, y, wavelength)
    mask_final.u = mask

    return mask_final, errors


def verify_mask(
    mask,
    z,
    has_mask,
    is_phase,
    is_binary,
    has_draw=False,
    has_axis=False,
    is_logarithm=True,
):

    """Computes the result of the algorithm in the far or near field. The mask is an amplitude mask.
    The mask can be one defined or one obtained from a
    If required it is converted to binary and/or phase

    Arguments:
        mask (Scalar_mask_XY): DOE to analyze
        z (None or float): If None computed at far field,else, distance for the near field
        has_mask (bool): If True, implements a circular pupil
        is_phase (bool): If True, converts the mask to a phase mask
        is_binary (bool): If True, converts the mask to a binary mask
        has_draw (bool): If True, draw the result
        has_axis (bool): If True, implements axis, else, it is removed
        is_logarithm (bool): If True, performs a logarithm on intensity
    Returns:
        DOE_new (Scalar_mask_XY): Result mask of algorithm (binarized, phase, etc.)
        result (np.array): propagation of the mask
    """

    DOE_new = deepcopy(mask)

    radius_x = (DOE_new.x.max() - DOE_new.x.min()) / 2
    radius_y = (DOE_new.y.max() - DOE_new.y.min()) / 2
    x_mean = (DOE_new.x.max() + DOE_new.x.min()) / 2
    y_mean = (DOE_new.y.max() + DOE_new.y.min()) / 2

    if is_phase:
        if is_binary:
            DOE_new.u = np.exp(1j * np.pi * DOE_new.u)
        else:
            DOE_new.u = np.exp(2j * np.pi * DOE_new.u)

    if has_mask:
        circle = Scalar_mask_XY(mask.x, mask.y, mask.wavelength)
        circle.circle(r0=(x_mean, y_mean), radius=(radius_x, radius_y))
        DOE_new = DOE_new * circle

    if z is None or z == 0:
        result = DOE_new.fft(new_field=True, shift=True, remove0=True)

    else:
        result = DOE_new.RS(z=z, new_field=True)

    if is_phase:
        code = "p"
    else:
        code = "a"

    if has_draw:
        result.draw(logarithm=is_logarithm)
        plt.axis("off")
        if has_axis is True:
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        else:
            intensity = np.abs(result.u) ** 2
            if is_logarithm:
                intensity = np.log(intensity + is_logarithm)

    return DOE_new, result


def nmse(I_result, I_target):
    """
    Computer the error as the average difference of the absolute value between of the intensity at target and the intensity at the result.

    Parameters:
        I_result (numpy.array): intensity produced by the algorithms
        I_target (numpy.array): intentisty at target
        is_balanced (bool): If True, perform the comparison using a proportion parameter to avoid different intensity levels

    Reference:
        K. Jahn and N. Bokor, “Intensity control of the focal spot by vectorial beam shaping,” Opt. Commun., vol. 283, no. 24, pp. 4859–4865, 2010, doi: 10.1016/j.optcom.2010.07.030.
        Similar to Ec. 17

    Returns:
        error: Mean difference between result and target.

    """

    error = np.sqrt(
        ((I_result / I_result.mean() - I_target / I_target.mean()) ** 2).mean()
    )

    return error


def binarize(mask, level=0.5):
    """
    Binarizes a (0,1), mask:
    """
    mask_new = np.zeros_like(mask, dtype=complex)
    mask_new[mask > level] = 1.0
    mask_new[mask <= level] = 0.0
    return mask_new
