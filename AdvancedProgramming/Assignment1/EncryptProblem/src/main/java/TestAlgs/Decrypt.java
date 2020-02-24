/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package TestAlgs;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

/**
 *
 * @author Giulio Purgatorio <giulio.purgatorio93 at gmail.com>
 */
/* Rewrite the source code of the @Encrypt and 
@Decrypt annotations, making them visible at runtime */

@Retention(RetentionPolicy.RUNTIME)
@interface Decrypt {
    String value() default "";
}

