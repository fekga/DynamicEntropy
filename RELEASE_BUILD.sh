#!/bin/bash
set -e # stop at error

versionTag=$1

if [ $versionTag ]; then
    currentBranch=$(git rev-parse --abbrev-ref HEAD)
    if [ $currentBranch != "main" ]; then
        echo "Please be on the \'main\' branch!"
        exit
    else
        echo "*********************************************"
        echo "*******************WARNING*******************"
        echo "*********************************************"
        echo "ALL OF YOUR NOT COMMITED CHANGES WILL BE LOST!"
        echo "MAKE SURE YOU DON\'T HAVE ANY IMPORTANT CHANGES!"
        echo "Changed and not commited files:"
        git diff --name-status
        read -p "Are you sure theye are not important? (y/n)" -n 1 -r
        echo    # (optional) move to a new line
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Aborted"
            exit 1
        fi
        
        git reset --hard HEAD
        git tag $versionTag
        git checkout master
        git merge $currentBranch
        python3 start.py noServer
        git commit -a -m "* generated files"
        git checkout $currentBranch
        git push --tags origin master $currentBranch
        echo "FINISHED"
    fi
   
else
    echo "Please give the VERSION TAG as parameter!";
    tagNumber=5;
    echo "The latest $tagNumber tag were:";
    git describe --tags `git rev-list --tags --max-count=$tagNumber`
    exit
fi
