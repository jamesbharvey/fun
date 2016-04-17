
;; make emacs start in the home directory
;; on windows esp - in windows need to set
;; this env var
(setq default-directory (getenv "HOME"))

(load-file ".emacs.small.el")


;; Added by Package.el.  This must come before configurations of
;; installed packages.  Don't delete this line.  If you don't want it,
;; just comment it out by adding a semicolon to the start of the line.
;; You may delete these explanatory comments.
(package-initialize)
(add-to-list 'package-archives '("marmalade" . "https://marmalade-repo.org/packages/"))
(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/"))
(add-to-list 'package-archives '("org" . "http://orgmode.org/elpa/") t)

;; Make our default background gray
;;(add-to-list 'default-frame-alist '(background-color . "lightgray"))

;; disabling keybinds of ergoemacs and cua modez
;;(ergoemacs-mode 0)
;;(cua-mode 0)


(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(ansi-color-names-vector
   ["#242424" "#e5786d" "#95e454" "#cae682" "#8ac6f2" "#333366" "#ccaa8f" "#f6f3e8"])
 '(column-number-mode t)
 '(custom-enabled-themes (quote (wombat)))
 '(custom-safe-themes
   (quote
    ("ad5a94f521d7907444d5febccffecf87db141eb1ea20bf89b03cce978146826a" "1edc234e0d44006b917995fddcc5e41ca7906df52cb622dd6f42f4357d29799f" "5cddc0334851dca08c4b6da925edef5bb4cf8820b3c64264aef31e0dc48587d9" "118570edb22c68e7295bbda8ae892efcc5fc319c4dfd29324d88be2779fbcdfc" "f3b838031ef46ae7fd0ec69aa78f411ee5e2e7135d2c661d7ab3b226f1271726" default)))
 '(inhibit-startup-screen t)
 '(package-selected-packages (quote (powershell yaml-mode ergoemacs-mode))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
